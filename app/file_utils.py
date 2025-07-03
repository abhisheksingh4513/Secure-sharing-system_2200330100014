import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from pathlib import Path
from decouple import config

# Configuration
UPLOAD_DIRECTORY = config("UPLOAD_DIRECTORY", default="./uploads")
MAX_FILE_SIZE = int(config("MAX_FILE_SIZE", default="50000000"))  # 50MB
ALLOWED_EXTENSIONS = config("ALLOWED_EXTENSIONS", default="pptx,docx,xlsx").split(",")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def validate_file_type(filename: str) -> bool:
    """Validate if the file type is allowed"""
    file_extension = filename.split('.')[-1].lower()
    return file_extension in ALLOWED_EXTENSIONS

def validate_file_size(file_size: int) -> bool:
    """Validate if the file size is within limits"""
    return file_size <= MAX_FILE_SIZE

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving the extension"""
    file_extension = original_filename.split('.')[-1]
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{file_extension}"

async def save_upload_file(upload_file: UploadFile) -> tuple[str, str, int]:
    """
    Save uploaded file to disk
    Returns: (saved_filename, file_path, file_size)
    """
    # Validate file type
    if not validate_file_type(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Only {', '.join(ALLOWED_EXTENSIONS)} files are permitted."
        )
    
    # Read file content
    content = await upload_file.read()
    file_size = len(content)
    
    # Validate file size
    if not validate_file_size(file_size):
        raise HTTPException(
            status_code=400,
            detail=f"File size too large. Maximum size allowed is {MAX_FILE_SIZE / (1024*1024):.1f} MB"
        )
    
    # Generate unique filename
    saved_filename = generate_unique_filename(upload_file.filename)
    file_path = os.path.join(UPLOAD_DIRECTORY, saved_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return saved_filename, file_path, file_size

def delete_file(file_path: str) -> bool:
    """Delete file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False

def get_file_info(file_path: str) -> Optional[dict]:
    """Get file information"""
    try:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime
            }
        return None
    except Exception:
        return None

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"
