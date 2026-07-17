import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.settings import settings


class Logger:
    """Centralized logger with rotating file handler."""
    
    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if self._logger is not None:
            return
        
        self._logger = logging.getLogger("kandy_ai")
        self._logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler with rotation
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "kandy_ai.log"
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)
    
    @property
    def logger(self) -> logging.Logger:
        return self._logger
    
    def info(self, message: str) -> None:
        self._logger.info(message)
    
    def debug(self, message: str) -> None:
        self._logger.debug(message)
    
    def warning(self, message: str) -> None:
        self._logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        self._logger.critical(message, exc_info=exc_info)


logger = Logger()
