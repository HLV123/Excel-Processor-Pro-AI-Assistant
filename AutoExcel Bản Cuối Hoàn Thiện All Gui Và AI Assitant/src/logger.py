import logging
from pathlib import Path
from typing import Optional
from config import Config

class Logger:
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        Config.setup_directories()
        
        self._logger = logging.getLogger("ExcelProcessor")
        self._logger.setLevel(Config.LOG_CONFIG["level"])
        
        if not self._logger.handlers:
            file_handler = logging.FileHandler(Config.LOG_CONFIG["filename"])
            console_handler = logging.StreamHandler()
            
            formatter = logging.Formatter(Config.LOG_CONFIG["format"])
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        return self._logger