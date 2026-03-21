# 📧 EMAILMIKE - Refactorización SOLID

## 📖 Sobre el Proyecto

Este proyecto es el resultado de una refactorización profunda de un sistema de envío de emails originalmente implementado como una clase monolítica. El objetivo principal fue aplicar los **principios SOLID** para obtener un código más mantenible, testeable y extensible.

## 🎯 Objetivo de la Refactorización

Transformar un servicio de email único y rígido en un sistema modular donde cada componente tenga una única responsabilidad y pueda ser extendido sin modificar el código existente.

## 🏗️ Arquitectura Refactorizada

### Estructura de Paquetes
EMAILMIKE/
├── config/ # Configuración del servidor y cuentas
│ └── email_config.py # Clases de configuración (SRP)
├── interfaces/ # Abstracciones (DIP)
│ └── email_interfaces.py # Interfaces: EmailProvider, MessageFormatter, EmailValidator
├── providers/ # Implementaciones concretas de proveedores (OCP)
│ └── smtp_providers.py # SMTPEmailProvider, MockEmailProvider
├── formatters/ # Formateadores de mensajes (OCP)
│ └── message_formatters.py # Text, HTML, JSON + Factory
├── services/ # Servicio principal (SRP, DIP)
│ └── email_service.py # EmailService (coordina dependencias)
├── utils/ # Utilidades
│ └── validators.py # EmailRegexValidator (SRP)
├── main.py # Ejemplo de uso
└── test.py # Pruebas


## 🔧 Principios SOLID Aplicados

### 1. **S**ingle Responsibility Principle (SRP) - Principio de Responsabilidad Única

**Antes:** Una sola clase `EmailService` manejaba configuración, conexión, validación, formato y envío.

**Después:** Cada clase tiene una única responsabilidad:

| Clase | Responsabilidad |
|-------|-----------------|
| `EmailConfiguration` | Configuración del servidor y cuenta |
| `EmailRegexValidator` | Validación de emails |
| `TextMessageFormatter` | Formateo de mensajes de texto |
| `HTMLMessageFormatter` | Formateo de mensajes HTML |
| `SMTPEmailProvider` | Conexión y envío SMTP |
| `EmailService` | Coordinar el flujo de envío |

### 2. **O**pen/Closed Principle (OCP) - Principio Abierto/Cerrado

**Antes:** Para añadir un nuevo formato de mensaje, había que modificar la clase principal.

**Después:** El sistema está abierto para extensión pero cerrado para modificación.

```python
# CÓMO EXTENDER - Sin modificar código existente
class PDFMessageFormatter(MessageFormatter):
    def format_message(self, from_addr, to_addr, subject, body) -> str:
        # Implementación para PDF
        return pdf_content

# Registrar el nuevo formateador
MessageFormatterFactory.register_formatter('pdf', PDFMessageFormatter())

#3. Liskov Substitution Principle (LSP) - Principio de Sustitución de Liskov
# Cualquier proveedor puede ser intercambiado
provider = SMTPEmailProvider(config)      # Real
provider = MockEmailProvider()            # Para pruebas

# Cualquier formateador puede ser intercambiado
formatter = TextMessageFormatter()        # Texto plano
formatter = HTMLMessageFormatter()        # HTML
formatter = JSONMessageFormatter()        # JSON

# El servicio funciona igual con cualquiera
service = EmailService(provider, validator, formatter)

#4. Interface Segregation Principle (ISP) - Principio de Segregación de Interfaces
# interfaces/email_interfaces.py
class EmailProvider(ABC):
    @abstractmethod
    def connect(self) -> bool: ...
    @abstractmethod
    def disconnect(self) -> bool: ...
    @abstractmethod
    def send_email(self, from_addr, to_addr, message) -> bool: ...

class MessageFormatter(ABC):
    @abstractmethod
    def format_message(self, from_addr, to_addr, subject, body) -> str: ...

class EmailValidator(ABC):
    @abstractmethod
    def validate_email(self, email: str) -> bool: ...

#5. Dependency Inversion Principle (DIP) - Principio de Inversión de Dependencias
Antes: EmailService dependía directamente de clases concretas (SMTP, validación específica, etc.)

Después: EmailService depende de abstracciones (interfaces), no de implementaciones concretas.

class EmailService:
    def __init__(
        self,
        provider: EmailProvider,        # Depende de abstracción
        validator: EmailValidator,      # Depende de abstracción
        default_formatter: MessageFormatter = None  # Depende de abstracción
    ):
        self._provider = provider
        self._validator = validator
        self._default_formatter = default_formatter or TextMessageFormatter()

🔄 Flujo del Sistema Refactorizado

1. Configuración (EmailConfiguration)
   ↓
2. Proveedor (SMTPEmailProvider)
   ↓
3. Validador (EmailRegexValidator) → Service (EmailService) ← Formateador (Text/HTML/JSON)
   ↓
4. Envío de email

Evidencia
<img width="905" height="681" alt="image" src="https://github.com/user-attachments/assets/6da311fa-968f-4a60-b4df-ffb152a425bd" />


🔗 Referencias
Principios SOLID explicados

Refactoring Guru - SOLID
