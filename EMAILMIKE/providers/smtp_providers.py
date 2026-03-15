import smtplib
import logging
from typing import Optional
from interfaces.email_interfaces import EmailProvider
from config.email_config import EmailConfiguration

logger = logging.getLogger(__name__)

class SMTPEmailProvider(EmailProvider):
    """Proveedor de email usando SMTP"""
    
    def __init__(self, config: EmailConfiguration):
        self.config = config
        self.server: Optional[smtplib.SMTP] = None
        self.is_connected = False
    
    def connect(self) -> bool:
        """Establece conexión con el servidor SMTP"""
        try:
            if self.config.server_config.use_ssl:
                self.server = smtplib.SMTP_SSL(
                    self.config.server_config.host,
                    self.config.server_config.port
                )
            else:
                self.server = smtplib.SMTP(
                    self.config.server_config.host,
                    self.config.server_config.port
                )
            
            if self.config.server_config.use_tls and not self.config.server_config.use_ssl:
                self.server.starttls()
            
            self.server.login(
                self.config.account_config.username,
                self.config.account_config.password
            )
            self.is_connected = True
            logger.info(f"Conectado exitosamente a {self.config.server_config.host}")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a {self.config.server_config.host}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> bool:
        """Cierra la conexión SMTP"""
        if self.server and self.is_connected:
            try:
                self.server.quit()
                self.is_connected = False
                logger.info("Conexión cerrada correctamente")
                return True
            except Exception as e:
                logger.error(f"Error cerrando conexión: {e}")
                return False
        return True
    
    def send_email(self, from_addr: str, to_addr: str, message: str) -> bool:
        """Envía un email usando el proveedor SMTP"""
        if not self.is_connected:
            if not self.connect():
                return False
        
        try:
            self.server.sendmail(from_addr, to_addr, message)
            logger.info(f"Email enviado correctamente a {to_addr}")
            return True
        except Exception as e:
            logger.error(f"Error enviando email a {to_addr}: {e}")
            return False


class MockEmailProvider(EmailProvider):
    """Proveedor mock para pruebas"""
    
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.sent_emails = []
    
    def connect(self) -> bool:
        return not self.should_fail
    
    def disconnect(self) -> bool:
        return True
    
    def send_email(self, from_addr: str, to_addr: str, message: str) -> bool:
        if self.should_fail:
            return False
        
        self.sent_emails.append({
            'from': from_addr,
            'to': to_addr,
            'message': message
        })
        return True