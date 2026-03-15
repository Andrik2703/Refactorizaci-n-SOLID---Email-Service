"""
Script de diagnóstico para verificar que todo está correcto
"""

import sys
import os

print("=" * 60)
print("🔍 DIAGNÓSTICO DEL SISTEMA EMAILMIKE")
print("=" * 60)

# Verificar estructura de carpetas
carpetas = ['config', 'formatters', 'interfaces', 'providers', 'services', 'utils']
print("\n📁 VERIFICANDO CARPETAS:")
for carpeta in carpetas:
    if os.path.exists(carpeta):
        print(f"   ✅ {carpeta}/")
    else:
        print(f"   ❌ {carpeta}/ (NO EXISTE)")

# Verificar archivos __init__.py
print("\n📄 VERIFICANDO __init__.py:")
for carpeta in carpetas:
    init_file = os.path.join(carpeta, '__init__.py')
    if os.path.exists(init_file):
        print(f"   ✅ {carpeta}/__init__.py")
    else:
        print(f"   ❌ {carpeta}/__init__.py (NO EXISTE)")

# Verificar archivos principales
archivos = [
    'config/email_config.py',
    'formatters/message_formatters.py',
    'interfaces/email_interfaces.py',
    'providers/smtp_providers.py',
    'services/email_service.py',
    'utils/validators.py',
    'main.py',
    'test.py'
]

print("\n📄 VERIFICANDO ARCHIVOS PRINCIPALES:")
for archivo in archivos:
    if os.path.exists(archivo):
        tamaño = os.path.getsize(archivo)
        print(f"   ✅ {archivo} ({tamaño} bytes)")
    else:
        print(f"   ❌ {archivo} (NO EXISTE)")

# Probar importaciones
print("\n🔌 PROBANDO IMPORTACIONES:")

try:
    from config import EmailConfiguration
    print("   ✅ from config import EmailConfiguration")
except Exception as e:
    print(f"   ❌ config: {e}")

try:
    from providers import SMTPEmailProvider
    print("   ✅ from providers import SMTPEmailProvider")
except Exception as e:
    print(f"   ❌ providers: {e}")

try:
    from services import EmailService
    print("   ✅ from services import EmailService")
except Exception as e:
    print(f"   ❌ services: {e}")

try:
    from formatters import TextMessageFormatter
    print("   ✅ from formatters import TextMessageFormatter")
except Exception as e:
    print(f"   ❌ formatters: {e}")

try:
    from utils import EmailRegexValidator
    print("   ✅ from utils import EmailRegexValidator")
except Exception as e:
    print(f"   ❌ utils: {e}")

print("\n" + "=" * 60)
print("Para obtener contraseña de aplicación de Gmail:")
print("1. Ve a https://myaccount.google.com/")
print("2. Seguridad → Verificación en dos pasos")
print("3. Busca 'Contraseñas de aplicaciones'")
print("4. Genera una nueva contraseña para 'Python SMTP'")
print("=" * 60)
input("\nPresiona Enter para salir...")