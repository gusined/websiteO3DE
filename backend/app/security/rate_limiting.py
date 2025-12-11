import time
from collections import defaultdict
from fastapi import HTTPException, Request
from typing import Dict, List
import hashlib

class RateLimiter:
    def init(self):
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.failed_logins: Dict[str, List[float]] = defaultdict(list)
        self.blocked_ips: Dict[str, float] = {}

    def is_blocked(self, identifier: str) -> bool:
        """Проверка, заблокирован ли идентификатор"""
        block_time = self.blocked_ips.get(identifier)
        if block_time and time.time() - block_time < 3600:  
            return True
        return False

    def check_rate_limit(self, 
                        identifier: str, 
                        max_requests: int, 
                        window: int,
                        endpoint: str = None) -> bool:
        """Проверка rate limit"""
        
        if self.is_blocked(identifier):
            return False

        now = time.time()
        key = f"{identifier}:{endpoint}" if endpoint else identifier
        
        self.requests[key] = [req_time for req_time in self.requests[key] 
                             if now - req_time < window]
        
        if len(self.requests[key]) >= max_requests:
            if len(self.requests[key]) >= max_requests * 2:
                self.blocked_ips[identifier] = now
            return False
        
        self.requests[key].append(now)
        return True

    def record_failed_login(self, identifier: str):
        """Запись неудачной попытки входа"""
        now = time.time()
        self.failed_logins[identifier].append(now)
        
        self.failed_logins[identifier] = [
            attempt for attempt in self.failed_logins[identifier] 
            if now - attempt < 900
        ]
        
        if len(self.failed_logins[identifier]) > 5:
            self.blocked_ips[identifier] = now

    def get_remaining_attempts(self, identifier: str) -> int:
        """Получение оставшихся попыток входа"""
        return max(0, 5 - len(self.failed_logins.get(identifier, [])))

rate_limiter = RateLimiter()

def rate_limit(max_requests: int = 100, window: int = 60, endpoint: str = None):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            identifier = get_client_identifier(request)
            
            if not rate_limiter.check_rate_limit(identifier, max_requests, window, endpoint):
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

def get_client_identifier(request: Request) -> str:
    """Получение идентификатора клиента"""
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    identifier_data = f"{client_ip}:{user_agent}"
    return hashlib.sha256(identifier_data.encode()).hexdigest()