from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db, User
from ..schemas import UserCreate, UserLogin, UserResponse, Token, SignUpResponse, EmailVerificationRequest
from ..auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    create_email_verification_token,
    verify_email_verification_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..email_service import email_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=SignUpResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Client user signup with email verification"""
    
    # Only allow client users to signup
    if user.user_type != "client":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only client users can signup through this endpoint"
        )
    
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user.password)
    verification_token = create_email_verification_token(user.email)
    
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        user_type=user.user_type,
        is_verified=False,
        verification_token=verification_token
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create verification URL
    verification_url = f"http://localhost:8000/auth/verify-email?token={verification_token}"
    
    # Send verification email
    email_sent = email_service.send_verification_email(user.email, verification_url)
    
    if not email_sent:
        # If email fails, still return success but log the issue
        pass
    
    return SignUpResponse(
        message="User created successfully. Please check your email for verification.",
        verification_url=verification_url,
        user_id=db_user.id
    )

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email address"""
    
    # Verify token
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return {"message": "Email already verified"}
    
    # Update user verification status
    user.is_verified = True
    user.verification_token = None
    db.commit()
    
    return {"message": "Email verified successfully"}

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified. Please check your email and verify your account."
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/manual-verify/{user_id}")
async def manual_verify_user(user_id: int, db: Session = Depends(get_db)):
    """Manually verify a user (for demo purposes)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        return {"message": "User already verified"}
    
    user.is_verified = True
    user.verification_token = None
    db.commit()
    
    return {"message": "User verified successfully"}

@router.post("/ops-login", response_model=Token)
async def ops_login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Operations user login (manual verification for ops users)"""
    
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.user_type != "ops":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for operations users"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
