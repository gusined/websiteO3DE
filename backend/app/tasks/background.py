from fastapi import BackgroundTasks
from app.utils.email import email_service

async def send_welcome_email(user_email: str, username: str):
    """Фоновая задача для отправки приветственного email"""
    subject = "Welcome to Our Platform!"
    body = f"""
    Hello {username}!
    
    Welcome to our platform. We're excited to have you on board.
    
    Best regards,
    The Team
    """
    
    await email_service.send_email(user_email, subject, body)

async def cleanup_temp_files(file_paths: list):
    """Фоновая задача для очистки временных файлов"""
    import os
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")