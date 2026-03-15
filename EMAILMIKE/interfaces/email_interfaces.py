from abc import ABC, abstractmethod
from typing import Optional

class EmailProvider(ABC):
    """Interfaz para proveedores de email"""
    
    @abstractmethod
    def send_email(self, from_addr: str, to_addr: str, message: str) -> bool:
        """Envía un email usando el proveedor específico"""
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con el proveedor"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Cierra la conexión con el proveedor"""
        pass


class MessageFormatter(ABC):
    """Interfaz para formateadores de mensajes"""
    
    @abstractmethod
    def format_message(self, from_addr: str, to_addr: str, subject: str, body: str) -> str:
        """Formatea el mensaje según el tipo específico"""
        pass


class EmailValidator(ABC):
    """Interfaz para validadores de email"""
    
    @abstractmethod
    def validate_email(self, email: str) -> bool:
        """Valida una dirección de email"""
        pass