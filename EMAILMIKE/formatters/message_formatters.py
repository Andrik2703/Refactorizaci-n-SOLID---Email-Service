from interfaces.email_interfaces import MessageFormatter
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

class TextMessageFormatter(MessageFormatter):
    """Formateador para mensajes de texto plano"""
    
    def format_message(self, from_addr: str, to_addr: str, subject: str, body: str) -> str:
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        return msg.as_string()


class HTMLMessageFormatter(MessageFormatter):
    """Formateador para mensajes HTML"""
    
    def __init__(self, template: str = None):
        self.template = template or self._default_template()
    
    def _default_template(self) -> str:
        return """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #4285F4;">Notificación</h2>
                <p>{body}</p>
                <hr>
                <small style="color: #666;">Este es un mensaje automático</small>
            </body>
        </html>
        """
    
    def format_message(self, from_addr: str, to_addr: str, subject: str, body: str) -> str:
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        
        html_body = self.template.format(body=body)
        msg.attach(MIMEText(html_body, 'html'))
        return msg.as_string()


class JSONMessageFormatter(MessageFormatter):
    """Formateador para mensajes JSON (ejemplo de extensibilidad)"""
    
    def format_message(self, from_addr: str, to_addr: str, subject: str, body: str) -> str:
        import json
        data = {
            'from': from_addr,
            'to': to_addr,
            'subject': subject,
            'body': body,
            'timestamp': '2024-01-01T00:00:00'  # Simplificado
        }
        return json.dumps(data)


class MessageFormatterFactory:
    """Factory para crear formateadores"""
    
    _formatters: Dict[str, MessageFormatter] = {
        'text': TextMessageFormatter(),
        'html': HTMLMessageFormatter(),
        'json': JSONMessageFormatter()
    }
    
    @classmethod
    def get_formatter(cls, format_type: str) -> MessageFormatter:
        """Obtiene un formateador por tipo"""
        if format_type not in cls._formatters:
            raise ValueError(f"Formato no soportado: {format_type}")
        return cls._formatters[format_type]
    
    @classmethod
    def register_formatter(cls, name: str, formatter: MessageFormatter):
        """Registra un nuevo formateador (OCP en acción)"""
        cls._formatters[name] = formatter