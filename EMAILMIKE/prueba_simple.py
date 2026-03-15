"""
Prueba con limpieza automática de espacios
"""
EMAIL = "b.condeleal@gmail.com"
PASSWORD = "dflk hmou jupz otmb"  # Escrita manualmente

# Limpiamos la contraseña de espacios extras al inicio y final
PASSWORD_LIMPIA = PASSWORD.strip()

print(f"Email: {EMAIL}")
print(f"Password original: '{PASSWORD}'")
print(f"Longitud original: {len(PASSWORD)}")
print(f"Password limpia: '{PASSWORD_LIMPIA}'")
print(f"Longitud limpia: {len(PASSWORD_LIMPIA)}")

import smtplib

try:
    print("\nConectando a Gmail...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    print("Iniciando sesión...")
    server.login(EMAIL, PASSWORD_LIMPIA)
    print("✅ LOGIN EXITOSO!")
    server.quit()
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Tipo: {type(e).__name__}")

input("\nPresiona Enter para salir...")