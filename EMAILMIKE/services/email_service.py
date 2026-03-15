import logging
from typing import Optional, Dict, Any

from interfaces.email_interfaces import EmailProvider, MessageFormatter, EmailValidator
from providers.smtp_providers import SMTPEmailProvider
from formatters.message_formatters import MessageFormatterFactory
from utils.validators import EmailRegexValidator
from config.email_config import EmailConfiguration

logger = logging.getLogger(__name__)

class EmailService:
    """
    Servicio principal de envío de emails.
    Sigue SRP: Solo coordina las diferentes responsabilidades.
    """
    
    def __init__(
        self,
        provider: EmailProvider,
        validator: Optional[EmailValidator] = None,
        default_formatter: Optional[MessageFormatter] = None
    ):
        self.provider = provider
        self.validator = validator or EmailRegexValidator()
        self.default_formatter = default_formatter or MessageFormatterFactory.get_formatter('text')
        self._connected = False
    
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        from_addr: Optional[str] = None,
        formatter: Optional[MessageFormatter] = None,
        auto_connect: bool = True
    ) -> bool:
        """
        Envía un email con todas las validaciones necesarias
        
        Args:
            recipient: Dirección del destinatario
            subject: Asunto del email
            body: Cuerpo del mensaje
            from_addr: Dirección remitente (opcional)
            formatter: Formateador específico (opcional)
            auto_connect: Conectar automáticamente si es necesario
        
        Returns:
            bool: True si el envío fue exitoso
        """
        # 1. Validar destinatario
        if not self.validator.validate_email(recipient):
            logger.error(f"Dirección de destinatario inválida: {recipient}")
            return False
        
        # 2. Validar remitente si se proporciona
        if from_addr and not self.validator.validate_email(from_addr):
            logger.error(f"Dirección de remitente inválida: {from_addr}")
            return False
        
        # 3. Usar formateador proporcionado o el por defecto
        message_formatter = formatter or self.default_formatter
        
        # 4. Formatear mensaje
        try:
            message = message_formatter.format_message(
                from_addr or self._get_default_from(),
                recipient,
                subject,
                body
            )
        except Exception as e:
            logger.error(f"Error formateando mensaje: {e}")
            return False
        
        # 5. Enviar email
        if auto_connect and not self._connected:
            if not self.provider.connect():
                return False
            self._connected = True
        
        result = self.provider.send_email(
            from_addr or self._get_default_from(),
            recipient,
            message
        )
        
        return result
    
    def _get_default_from(self) -> str:
        """Obtiene dirección remitente por defecto"""
        if hasattr(self.provider, 'config'):
            return self.provider.config.account_config.default_from
        return "default@example.com"
    
    def disconnect(self):
        """Cierra la conexión con el proveedor"""
        if self._connected:
            self.provider.disconnect()
            self._connected = False
    
    def __enter__(self):
        """Soporte para context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión al salir del context manager"""
        self.disconnect()