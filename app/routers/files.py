from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import os
import os

from ..database import get_db, User, FileUpload, DownloadToken
from ..schemas import FileUploadResponse, FileListResponse, DownloadResponse
from ..auth import get_ops_user, get_client_user, generate_secure_download_token
from ..file_utils import save_upload_file

router = APIRouter(prefix="/files", tags=["File Operations"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_ops_user),
    db: Session = Depends(get_db)
):
    """Upload file (Only for Operations users)"""
    
    # Save file to disk
    saved_filename, file_path, file_size = await save_upload_file(file)
    
    # Get file type
    file_type = file.filename.split('.')[-1].lower()
    
    # Create file record in database
    db_file = FileUpload(
        filename=saved_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type,
        uploader_id=current_user.id
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return FileUploadResponse(
        id=db_file.id,
        filename=db_file.filename,
        original_filename=db_file.original_filename,
        file_size=db_file.file_size,
        file_type=db_file.file_type,
        upload_date=db_file.upload_date,
        message="File uploaded successfully"
    )

@router.get("/list", response_model=List[FileListResponse])
async def list_files(
    current_user: User = Depends(get_client_user),
    db: Session = Depends(get_db)
):
    """List all uploaded files (Only for Client users)"""
    
    files = db.query(FileUpload).join(User).all()
    
    return [
        FileListResponse(
            id=file.id,
            filename=file.filename,
            original_filename=file.original_filename,
            file_size=file.file_size,
            file_type=file.file_type,
            upload_date=file.upload_date,
            uploader_username=file.uploader.username
        )
        for file in files
    ]

@router.get("/get-download-link/{file_id}", response_model=DownloadResponse)
async def get_download_link(
    file_id: int,
    current_user: User = Depends(get_client_user),
    db: Session = Depends(get_db)
):
    """Get secure download link for a file (Only for Client users)"""
    
    # Check if file exists
    file = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Generate secure download token
    download_token = generate_secure_download_token()
    
    # Set token expiration (1 hour from now)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Create download token record
    db_token = DownloadToken(
        token=download_token,
        file_id=file_id,
        user_id=current_user.id,
        expires_at=expires_at
    )
    
    db.add(db_token)
    db.commit()
    
    # Create secure download URL
    download_url = f"/files/secure-download/{download_token}"
    
    return DownloadResponse(
        download_link=download_url,
        message="success"
    )

@router.get("/secure-download/{token}")
async def download_file(
    token: str,
    db: Session = Depends(get_db)
):
    """Download file using secure token"""
    
    # Find download token
    download_token = db.query(DownloadToken).filter(
        DownloadToken.token == token,
        DownloadToken.is_used == False
    ).first()
    
    if not download_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired download link"
        )
    
    # Check if token has expired
    if download_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Download link has expired"
        )
    
    # Get file information
    file = db.query(FileUpload).filter(FileUpload.id == download_token.file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Mark token as used
    download_token.is_used = True
    db.commit()
    
    # Return file
    return FileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type='application/octet-stream'
    )

@router.get("/test-download/{file_id}")
async def test_download(file_id: int, db: Session = Depends(get_db)):
    """Test download endpoint for debugging"""
    # Get file information
    file = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check if file exists on disk
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found on disk: {file.file_path}"
        )
    
    # Return file
    return FileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type='application/octet-stream'
    )
