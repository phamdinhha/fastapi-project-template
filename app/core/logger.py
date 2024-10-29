import logging
import sys
from typing import Any, Optional
from pathlib import Path
from logging.handlers import RotatingFileHandler

class ServiceLogger:
    """Simple logger for service-wide use"""
    _instance: Optional[logging.Logger] = None

    @classmethod
    def setup(cls, 
              service_name: str = "service",
              log_file: str = "logs/service.log",
              level: str = "INFO") -> None:
        """Singleton to setup logger once at application startup"""
        if cls._instance is not None:
            return

        # Create logger
        logger = logging.getLogger(service_name)
        logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        try:
            # Create logs directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(exist_ok=True)

            # Setup file handler with rotation
            file_handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to setup file logging: {e}")

        cls._instance = logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the configured logger instance"""
        if cls._instance is None:
            cls.setup()
        return cls._instance
    
    @classmethod
    def debug(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message"""
        cls.get_logger().debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message"""
        cls.get_logger().info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message"""
        cls.get_logger().warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message"""
        cls.get_logger().error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message"""
        cls.get_logger().critical(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log exception message"""
        cls.get_logger().exception(msg, *args, **kwargs)