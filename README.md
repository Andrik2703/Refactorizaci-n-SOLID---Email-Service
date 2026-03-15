# Refactorizaci-n-SOLID---Email-Service
🐍 Actividad: Refactorización SOLID - Email Service
1. Investigación de Arquitectura:
Investigar y documentar con sus propias palabras los 5 principios SOLID. Deben explicar el problema que resuelve cada uno y cómo impacta en la escalabilidad de un proyecto real.
2. Ejemplo Maestro (DIP & SRP):
Observen cómo desacoplar un servicio mediante interfaces. El manager no depende de la implementación (Email o SMS), sino del contrato (MessageService).
from abc import ABC, abstractmethod # Interfaz: Define el QUÉ, no el CÓMO class MessageService(ABC): @abstractmethod def send(self, message: str, receiver: str): pass # Implementación: Aquí va la lógica específica class SimpleEmailService(MessageService): def send(self, message, receiver): print(f"Enviando Email a {receiver}: {message}") # Manager: Depende de la Abstracción (DIP) class NotificationManager: def __init__(self, service: MessageService): self.service = service def notify(self, msg, user): self.service.send(msg, user)
3. Reto: Refactorización del Repositorio "EMAILMIKE":
Clonen el código base del docente y analicen la clase EmailSender. Actualmente, esta clase mezcla configuración, formato y envío. Su misión es dejarla 100% SOLID.
📦 Repositorio a Refactorizar:
https://github.com/MikeCardona076/EMAILMIKE
Separar la configuración SMTP de la lógica de envío (SRP).
Crear una interfaz para que el sistema soporte otros proveedores en el futuro (DIP).
Asegurarse de que el código sea testeable y modular.
📸 Evidencias requeridas:
Documento PDF con la investigación teórica de los 5 principios.
Enlace a su propio repositorio con el código refactorizado.
Captura de pantalla de la terminal ejecutando el nuevo servicio de correo.
Formato de entrega:
Archivo PDF profesional con evidencias y links.
Seguir instrucciones acordadas en clase
💡 Tip de Mike:
"Recuerden que si para cambiar de Gmail a Outlook tienen que borrar y reescribir media clase, entonces no están aplicando SOLID. ¡Hagan que su código sea intercambiable!"
