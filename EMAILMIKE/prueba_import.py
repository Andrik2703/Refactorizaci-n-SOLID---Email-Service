print("=" * 50)
print("PRUEBA DE IMPORTACIONES")
print("=" * 50)

# Prueba 1: Importación directa
try:
    from config.email_config import EmailConfiguration
    print("✅ from config.email_config import EmailConfiguration")
except Exception as e:
    print(f"❌ Error en importación directa: {e}")

# Prueba 2: Importación desde el paquete
try:
    from config import EmailConfiguration
    print("✅ from config import EmailConfiguration")
except Exception as e:
    print(f"❌ Error en importación desde paquete: {e}")

# Prueba 3: Verificar qué hay en config.__init__
try:
    import config
    print(f"\n📁 Contenido de config:")
    print(f"   Dir: {dir(config)}")
    print(f"   __all__: {getattr(config, '__all__', 'No definido')}")
except Exception as e:
    print(f"❌ Error inspeccionando config: {e}")

print("\n" + "=" * 50)
input("Presiona Enter para salir...")