from fastapi import Request
from fastapi.responses import JSONResponse
import time
import re
from typing import Dict, List
import ipaddress

class SecurityMiddleware:
    def init(self):
        self.rate_limits: Dict[str, List[float]] = {}
        self.blocked_ips: set = set()
        self.suspicious_patterns = [
            r"<script.*?>.*?</script>",  # XSS
            r"(\bUNION\b.*\bSELECT\b)",  # SQL Injection
            r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b)",  # SQL commands
            r"(\.\./|\.\.\\\)",  # Path traversal
            r"eval\s*\(",  # Code injection
            r"system\s*\(",  # Command injection
        ]

    async def call(self, request: Request, call_next):
        client_ip = request.client.host
        
        if client_ip in self.blocked_ips:
            return JSONResponse(
                status_code=403,
                content={"detail": "IP address blocked"}
            )

        if not self.check_rate_limit(client_ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )

        if await self.detect_malicious_request(request):
            self.blocked_ips.add(client_ip)
            return JSONResponse(
                status_code=400,
                content={"detail": "Malicious request detected"}
            )

        response = await call_next(request)
        self.add_security_headers(response)
        
        return response

    def check_rate_limit(self, ip: str, max_requests: int = 100, window: int = 60) -> bool:
        """Rate limiting по IP адресу"""
        now = time.time()
        if ip not in self.rate_limits:
            self.rate_limits[ip] = []
        
        self.rate_limits[ip] = [timestamp for timestamp in self.rate_limits[ip] 
                               if now - timestamp < window]
        
        if len(self.rate_limits[ip]) >= max_requests:
            return False
        
        self.rate_limits[ip].append(now)
        return True

    async def detect_malicious_request(self, request: Request) -> bool:
        """Обнаружение подозрительных запросов"""
        
        for param, value in request.query_params.items():
            if self.contains_malicious_patterns(str(value)):
                return True

        if self.contains_malicious_patterns(request.url.path):
            return True

        if request.method in ["POST", "PUT"]:
            body = await request.body()
            if self.contains_malicious_patterns(body.decode('utf-8', errors='ignore')):
                return True

        return False

    def contains_malicious_patterns(self, text: str) -> bool:
        """Проверка на наличие вредоносных паттернов"""
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def add_security_headers(self, response):
        """Добавление security headers"""
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=()"
        }
        
        for header, value in security_headers.items():
            response.headers[header] = value