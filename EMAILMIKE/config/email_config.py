from dataclasses import dataclass
from typing import Optional

@dataclass
class EmailServerConfig:
    """Configuración del servidor de email"""
    host: str
    port: int
    use_tls: bool = True
    use_ssl: bool = False


@dataclass
class EmailAccountConfig:
    """Configuración de la cuenta de email"""
    username: str
    password: str
    default_from: Optional[str] = None


class EmailConfiguration:
    """Gestiona la configuración de email"""
    
    def __init__(self, server_config: EmailServerConfig, account_config: EmailAccountConfig):
        self.server_config = server_config
        self.account_config = account_config
    
    @classmethod
    def create_gmail_config(cls, username: str, app_password: str) -> 'EmailConfiguration':
        """Factory method para crear configuración de Gmail"""
        server_config = EmailServerConfig(
            host="smtp.gmail.com",
            port=587,
            use_tls=True,
            use_ssl=False
        )
        account_config = EmailAccountConfig(
            username=username,
            password=app_password.strip(),  # Limpia espacios invisibles
            default_from=username
        )
        return cls(server_config, account_config)
    
    @classmethod
    def create_outlook_config(cls, username: str, password: str) -> 'EmailConfiguration':
        """Factory method para crear configuración de Outlook"""
        server_config = EmailServerConfig(
            host="smtp-mail.outlook.com",
            port=587,
            use_tls=True,
            use_ssl=False
        )
        account_config = EmailAccountConfig(
            username=username,
            password=password,
            default_from=username
        )
        return cls(server_config, account_config)