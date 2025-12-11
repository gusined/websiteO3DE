import html
import bleach
from markdown import markdown
from fastapi import HTTPException

class XSSProtection:
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 's', 
        'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'a', 'blockquote', 'code', 'pre'
    ]
    
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title'],
    }

    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """Очистка HTML от потенциально опасного контента"""
        if not html_content:
            return html_content
            
        cleaned_html = bleach.clean(
            html_content,
            tags=XSSProtection.ALLOWED_TAGS,
            attributes=XSSProtection.ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        cleaned_html = bleach.linkify(cleaned_html, callbacks=[])
        
        return cleaned_html

    @staticmethod
    def escape_html(text: str) -> str:
        """Экранирование HTML символов"""
        return html.escape(text)

    @staticmethod
    def safe_markdown_to_html(markdown_text: str) -> str:
        """Безопасное преобразование Markdown в HTML"""
        if not markdown_text:
            return markdown_text
            
        html_content = markdown(markdown_text)
        
        return XSSProtection.sanitize_html(html_content)

    @staticmethod
    def validate_url(url: str) -> bool:
        """Валидация URL для защиты от XSS"""
        if not url:
            return False
            
        allowed_schemes = ['http', 'https']
        from urllib.parse import urlparse
        
        try:
            result = urlparse(url)
            return (result.scheme in allowed_schemes and 
                   result.netloc and 
                   '.' in result.netloc)
        except Exception:
            return False