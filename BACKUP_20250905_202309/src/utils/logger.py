import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """Sistema de logging para el proyecto"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # File handler
            if log_file:
                # Crear directorio de logs si no existe
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log de información"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log de error"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Log de advertencia"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
    
    def success(self, message: str):
        """Log de éxito"""
        self.logger.info(f"✅ {message}")
    
    def failure(self, message: str):
        """Log de fallo"""
        self.logger.error(f"❌ {message}")

def get_logger(name: str) -> Logger:
    """Obtener logger configurado"""
    from .config import config
    
    # Crear directorio de logs
    log_dir = os.path.join(config.get_project_root(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Archivo de log con fecha
    log_file = os.path.join(log_dir, f"automation_{datetime.now().strftime('%Y%m%d')}.log")
    
    return Logger(name, log_file)
