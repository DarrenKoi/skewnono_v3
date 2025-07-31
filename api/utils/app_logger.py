"""
Centralized logger configuration for the entire application.
This ensures all parts of the app (Flask, scheduler, background tasks) use the same logger.
"""
import os
from loguru import logger as loguru_logger
from .logger_manager import LoggerManager

# Singleton instance of LoggerManager
_log_manager = None
_logger = None

def get_app_logger():
    """
    Get the centralized application logger instance.
    This ensures all parts of the application use the same logger configuration.
    """
    global _log_manager, _logger
    
    if _logger is None:
        # Initialize the logger manager only once
        _log_manager = LoggerManager(
            log_name="skewnono_app",
            log_file_path="logs/skewnono_app.log",
            level=os.getenv('LOG_LEVEL', 'INFO'),
            mode="prod" if os.getenv('FLASK_ENV') == 'production' else "dev",
            console_level="INFO",
            retention="30 days",
            rotation="100 MB",
            json_format=os.getenv('FLASK_ENV') == 'production',
            enable_exception_logging=True,
            backtrace=True,
            diagnose=os.getenv('FLASK_ENV') != 'production'
            # Colors are now always enabled by default (simplified)
        )
        _logger = _log_manager.get_logger()
        
        # Add application startup log
        _logger.info("Application logger initialized", 
                    pid=os.getpid(),
                    log_file=_log_manager.log_file_path.absolute())
    
    return _logger

def get_task_logger(task_name: str):
    """
    Get a logger instance for a specific background task.
    This adds task context to all log messages.
    
    Args:
        task_name: Name of the background task
        
    Returns:
        Logger instance with task context
    """
    base_logger = get_app_logger()
    return base_logger.bind(task=task_name, task_type="scheduled")

def cleanup_logger():
    """
    Clean up the logger instance.
    Should be called when the application shuts down.
    """
    global _log_manager, _logger
    
    if _log_manager:
        _log_manager.cleanup()
        _log_manager = None
        _logger = None

# Create a convenience alias
logger = get_app_logger()