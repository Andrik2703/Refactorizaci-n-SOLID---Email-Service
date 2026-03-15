"""
Módulo de configuración para el sistema de email.
"""

from .email_config import EmailServerConfig, EmailAccountConfig, EmailConfiguration

__all__ = [
    'EmailServerConfig',
    'EmailAccountConfig',
    'EmailConfiguration'
]