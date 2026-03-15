"""
Script de prueba con mejor manejo de errores
"""

import logging
import sys
from config.email_config import EmailConfiguration
from providers.smtp_providers import SMTPEmailProvider
from services.email_service import EmailService
from formatters.message_formatters import TextMessageFormatter
from utils.validators import EmailRegexValidator

# Configurar logging para ver todos los detalles
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("📧 SISTEMA DE EMAIL SOLID - MODO DEBUG")
print("=" * 60)

# Configuración - ¡CAMBIAR ESTOS VALORES!
MI_CORREO = "b.condeleal@gmail.com"
MI_PASSWORD = "dflk hmou jupz otmb"

print(f"\n📝 Configurando para: {MI_CORREO}")
print(f"📝 Password length: {len(MI_PASSWORD)} caracteres")

try:
    # 1. Crear configuración
    print("\n1. Creando configuración...")
    config = EmailConfiguration.create_gmail_config(
        username=MI_CORREO,
        app_password=MI_PASSWORD
    )
    print(f"   ✅ Configuración creada: {config.server_config.host}:{config.server_config.port}")
    
    # 2. Crear proveedor
    print("\n2. Creando proveedor SMTP...")
    provider = SMTPEmailProvider(config)
    print("   ✅ Proveedor creado")
    
    # 3. Crear validador
    print("\n3. Creando validador...")
    validator = EmailRegexValidator()
    print("   ✅ Validador creado")
    
    # 4. Crear servicio
    print("\n4. Creando servicio...")
    service = EmailService(
        provider=provider,
        validator=validator,
        default_formatter=TextMessageFormatter()
    )
    print("   ✅ Servicio creado")
    
    # 5. Solicitar destinatario
    print("\n" + "-" * 40)
    destinatario = input("📨 Email del destinatario: ").strip()
    
    if not destinatario:
        print("❌ No ingresaste un destinatario")
        sys.exit(1)
    
    # 6. Validar destinatario
    print(f"\n5. Validando destinatario: {destinatario}")
    if not validator.validate_email(destinatario):
        print(f"❌ Email inválido: {destinatario}")
        sys.exit(1)
    print("   ✅ Email válido")
    
    # 7. Enviar email
    print("\n6. Enviando email...")
    print("   🔌 Conectando al servidor SMTP...")
    
    with service:
        resultado = service.send_email(
            recipient=destinatario,
            subject="Prueba desde CMD - Sistema SOLID",
            body="""¡Hola! 
            
Este es un mensaje de prueba del sistema de email refactorizado con principios SOLID.

Si recibes esto, significa que todo funciona correctamente.

Saludos,
El equipo de desarrollo"""
        )
    
    if resultado:
        print("\n" + "=" * 60)
        print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EL EMAIL")
        print("=" * 60)
        print("Revisa los mensajes de DEBUG arriba para más detalles")
        
except Exception as e:
    print(f"\n❌ Error inesperado: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
input("Presiona Enter para salir...")