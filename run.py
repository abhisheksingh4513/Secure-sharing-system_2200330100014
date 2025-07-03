#!/usr/bin/env python3
"""
Main application runner
"""

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("Starting Secure File Sharing System...")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )
