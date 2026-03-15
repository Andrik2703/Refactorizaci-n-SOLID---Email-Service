import re
import logging
from typing import List
from interfaces.email_interfaces import EmailValidator

logger = logging.getLogger(__name__)

class EmailRegexValidator(EmailValidator):
    """Validador de emails usando expresiones regulares"""
    
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate_email(self, email: str) -> bool:
        """Valida formato de email usando regex"""
        if not email or not isinstance(email, str):
            return False
        
        is_valid = bool(self.EMAIL_REGEX.match(email))
        if not is_valid:
            logger.warning(f"Email inválido: {email}")
        return is_valid


class CompositeEmailValidator(EmailValidator):
    """Validador compuesto que usa múltiples validadores"""
    
    def __init__(self, validators: List[EmailValidator]):
        self.validators = validators
    
    def validate_email(self, email: str) -> bool:
        """Valida email usando todos los validadores registrados"""
        for validator in self.validators:
            if not validator.validate_email(email):
                return False
        return True