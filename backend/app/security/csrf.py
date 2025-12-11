import secrets
from fastapi import Request, HTTPException
from typing import Optional

from backend.app.dependencies import get_current_user

class CSRFProtection:
    def init(self):
        self.tokens = {}

    def generate_csrf_token(self, user_id: str) -> str:
        """Генерация CSRF токена"""
        token = secrets.token_urlsafe(32)
        self.tokens[user_id] = token
        return token

    def validate_csrf_token(self, user_id: str, token: str) -> bool:
        """Валидация CSRF токена"""
        stored_token = self.tokens.get(user_id)
        if not stored_token or stored_token != token:
            return False
        return True

    def get_csrf_token_from_request(self, request: Request) -> Optional[str]:
        """Получение CSRF токена из запроса"""
        token = request.headers.get("X-CSRF-Token")
        if token:
            return token
            
        if request.method == "POST":
            form_data = dict(request.form())
            token = form_data.get("csrf_token")
            if token:
                return token
                
        return None

csrf_protection = CSRFProtection()

def csrf_protect(func):
    async def wrapper(request: Request, *args, **kwargs):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return await func(request, *args, **kwargs)
            
        user_id = get_current_user(request) 
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Authentication required")
            
        token = csrf_protection.get_csrf_token_from_request(request)
        if not token or not csrf_protection.validate_csrf_token(user_id, token):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")
            
        return await func(request, *args, **kwargs)
    return wrapper