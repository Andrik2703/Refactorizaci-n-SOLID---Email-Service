import logging
from config.email_config import EmailConfiguration
from providers.smtp_providers import SMTPEmailProvider, MockEmailProvider
from formatters.message_formatters import MessageFormatterFactory, HTMLMessageFormatter
from services.email_service import EmailService
from utils.validators import EmailRegexValidator

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Ejemplo de uso del sistema refactorizado
    """
    
    # Configuración (puede venir de variables de entorno)
    MI_CORREO = "tu_usuario@gmail.com"
    MI_APP_PASSWORD = "abcd efgh ijkl mnop"  # Contraseña de aplicación
    
    # 1. Crear configuración (SRP: Configuración separada)
    gmail_config = EmailConfiguration.create_gmail_config(
        username=MI_CORREO,
        app_password=MI_APP_PASSWORD
    )
    
    # 2. Crear proveedor (DIP: Dependencia de abstracción)
    provider = SMTPEmailProvider(gmail_config)
    
    # Alternativa para pruebas:
    # provider = MockEmailProvider()
    
    # 3. Crear validador (SRP: Validación separada)
    validator = EmailRegexValidator()
    
    # 4. Crear servicio (SRP: Coordinación)
    email_service = EmailService(
        provider=provider,
        validator=validator
    )
    
    # 5. Enviar email con diferentes formatos
    
    # Ejemplo 1: Texto plano
    with email_service:  # Usando context manager
        result = email_service.send_email(
            recipient="alumno_prueba@gmail.com",
            subject="Mensaje de prueba - Texto plano",
            body="Este es un mensaje de prueba en texto plano.",
            formatter=MessageFormatterFactory.get_formatter('text')
        )
        logger.info(f"Resultado envío texto: {result}")
    
    # Ejemplo 2: HTML (con formateador personalizado)
    html_formatter = HTMLMessageFormatter("""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h1 style="color: #34A853;">¡Hola!</h1>
                <p>{body}</p>
                <div style="background-color: #f0f0f0; padding: 10px;">
                    Mensaje personalizado
                </div>
            </body>
        </html>
    """)
    
    # Creamos nuevo servicio (o reutilizamos el anterior)
    new_service = EmailService(
        provider=SMTPEmailProvider(gmail_config),
        validator=validator,
        default_formatter=html_formatter
    )
    
    with new_service:
        result = new_service.send_email(
            recipient="alumno_prueba@gmail.com",
            subject="Mensaje de prueba - HTML personalizado",
            body="Este mensaje usa una plantilla HTML personalizada."
        )
        logger.info(f"Resultado envío HTML: {result}")

def test_with_mock():
    """Ejemplo de prueba con mock provider"""
    
    mock_provider = MockEmailProvider()
    validator = EmailRegexValidator()
    
    service = EmailService(
        provider=mock_provider,
        validator=validator
    )
    
    # Prueba de envío
    result = service.send_email(
        recipient="test@example.com",
        subject="Prueba",
        body="Mensaje de prueba"
    )
    
    logger.info(f"Prueba con mock: {result}")
    logger.info(f"Emails enviados: {len(mock_provider.sent_emails)}")

if __name__ == "__main__":
    main()
    # test_with_mock()  # Descomentar para probar con mock