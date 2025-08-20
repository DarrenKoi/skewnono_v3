"""
Standard logging configuration using Python's built-in logging module.
Cross-platform compatible using pathlib for Windows and Linux.
"""
import logging
import logging.handlers
import json
import re
import sys
import threading
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Union
from functools import wraps

# Thread lock for logger creation
_logger_lock = threading.Lock()

# Simple logger registry to track setup loggers
_setup_loggers = set()

# Cache for decorator loggers to avoid repeated quick_setup calls
_decorator_loggers = {}

# Constants for efficiency
STANDARD_FIELDS = frozenset({
    'name', 'msg', 'args', 'created', 'filename', 'funcName',
    'levelname', 'levelno', 'lineno', 'module', 'msecs',
    'pathname', 'process', 'processName', 'relativeCreated',
    'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
    'getMessage', 'message', 'asctime'
})

# Log levels mapping for efficient lookup
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Colorama import with proper error handling
try:
    import colorama
    colorama.init(autoreset=True)
    _COLORAMA_AVAILABLE = True
except ImportError:
    _COLORAMA_AVAILABLE = False


# Custom Formatters
class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'filename': record.filename,
            'pathname': record.pathname,
            'process': record.process,
            'process_name': record.processName,
            'thread': record.thread,
            'thread_name': record.threadName,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_obj['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # Add custom fields from extra parameter more efficiently
        for key, value in record.__dict__.items():
            if key not in STANDARD_FIELDS:
                log_obj[key] = self._serialize_value(value)
        
        return json.dumps(log_obj, ensure_ascii=False)
    
    @staticmethod
    def _serialize_value(value):
        """Efficiently serialize custom field values."""
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        try:
            return str(value)
        except Exception:
            return repr(value)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, fmt=None, datefmt=None, use_colors=True):
        super().__init__(fmt, datefmt)
        # Check if colors are supported
        self.use_colors = use_colors and sys.stderr.isatty()
        
        # On Windows, check if ANSI colors are supported
        if self.use_colors and sys.platform == 'win32':
            if not _COLORAMA_AVAILABLE:
                self.use_colors = False
    
    def format(self, record: logging.LogRecord) -> str:
        if self.use_colors:
            # Store original values to avoid expensive string replacements
            original_levelname = record.levelname
            original_msg = record.msg
            
            levelname = record.levelname
            if levelname in self.COLORS:
                color = self.COLORS[levelname]
                record.levelname = f"{color}{self.BOLD}{levelname}{self.RESET}"
                record.msg = f"{color}{record.msg}{self.RESET}"
        
        result = super().format(record)
        
        # Restore original values efficiently
        if self.use_colors:
            record.levelname = original_levelname
            record.msg = original_msg
        
        return result


class CompactFormatter(logging.Formatter):
    """Compact formatter for minimal output."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Format: [LEVEL] message (module:line)
        return f"[{record.levelname[0]}] {record.getMessage()} ({record.module}:{record.lineno})"


class DetailedFormatter(logging.Formatter):
    """Detailed formatter with extra context."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Get the base formatted message
        base_msg = super().format(record)
        
        # Add extra fields if any
        extra_fields = [
            f"{key}={value}" 
            for key, value in record.__dict__.items() 
            if key not in STANDARD_FIELDS
        ]
        
        if extra_fields:
            return f"{base_msg} | {' | '.join(extra_fields)}"
        
        return base_msg


def _setup_base_logger(root_dir: str, logging_name: str, level: str = "INFO") -> tuple:
    """
    Base function to set up common logger components.
    
    Returns:
        tuple: (log_dir, logger, level_upper)
    """
    # Validate root_dir
    if not root_dir:
        root_dir = str(Path.cwd())
    
    # Validate and sanitize logging_name
    if not logging_name:
        raise ValueError("logging_name cannot be empty")
    
    # Validate level
    level_upper = level.upper()
    if level_upper not in LOG_LEVELS:
        raise ValueError(f"Invalid log level: {level}. Must be one of {list(LOG_LEVELS.keys())}")
    
    # Create log directory using pathlib
    log_dir = Path(root_dir) / 'logging_info'
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise IOError(f"Failed to create log directory {log_dir}: {e}")
    
    # Create logger with thread safety
    with _logger_lock:
        # Check if this logger was already set up
        if logging_name in _setup_loggers:
            logger = logging.getLogger(logging_name)
            return log_dir, logger, level_upper
            
        logger = logging.getLogger(logging_name)
        
        # Prevent duplicate logs by checking if handlers already exist
        if logger.handlers:
            _setup_loggers.add(logging_name)
            return log_dir, logger, level_upper
        
        # Set logger level and disable propagation
        logger.setLevel(LOG_LEVELS[level_upper])
        logger.propagate = False
        
        # Mark as set up
        _setup_loggers.add(logging_name)
    
    return log_dir, logger, level_upper


def setup_logger(root_dir: str, logging_name: str, 
                 level: str = "INFO",
                 console_level: Optional[str] = None,
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB default
                 backup_count: int = 5,
                 log_format: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Name of the logger (also used for log file name)
        level: Logging level for file handler (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_level: Logging level for console handler (defaults to INFO)
        max_bytes: Maximum size of log file before rotation (default 10MB)
        backup_count: Number of backup files to keep (default 5)
        log_format: Custom log format string (optional)
    
    Returns:
        Configured logger instance
    
    Example:
        from api.utils.logging_config import setup_logger
        logger = setup_logger('/path/to/project', 'my_app')
        logger.info('Application started')
    """
    # Use base setup function for common setup
    log_dir, logger, level_upper = _setup_base_logger(root_dir, logging_name, level)
    
    # If logger already has handlers, return it
    if logger.handlers:
        return logger
    
    # Sanitize logging_name for file system (remove/replace invalid characters)
    safe_logging_name = re.sub(r'[<>:"/\\|?*]', '_', logging_name)
    
    # Define log format
    if log_format is None:
        log_format = '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Create file handler with rotation (use sanitized name)
    log_file = log_dir / f'{safe_logging_name}.log'
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),  # Convert Path to string for compatibility
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS[level_upper])
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_level_str = (console_level or level).upper()
    console_handler.setLevel(LOG_LEVELS[console_level_str])
    
    # Simpler format for console
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log initial message
    logger.info(f"Logger '{logging_name}' initialized - Log file: {log_file.absolute()}")
    
    return logger


def get_logger(logging_name: str) -> logging.Logger:
    """
    Get an existing logger by name.
    
    Args:
        logging_name: Name of the logger to retrieve
    
    Returns:
        Logger instance if it exists, None otherwise
    """
    return logging.getLogger(logging_name)


def cleanup_logger(logging_name: str):
    """
    Clean up a logger by removing all its handlers.
    
    Args:
        logging_name: Name of the logger to clean up
    """
    logger = logging.getLogger(logging_name)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    
    # Remove from setup registry
    with _logger_lock:
        _setup_loggers.discard(logging_name)


def setup_flask_logger(app, root_dir: str):
    """
    Set up logging for a Flask application.
    
    Args:
        app: Flask application instance
        root_dir: Root directory for log files
    
    Returns:
        Tuple of (app_logger, request_logger, error_logger)
    
    Example:
        from flask import Flask
        from api.utils.logging_config import setup_flask_logger
        
        app = Flask(__name__)
        app_logger, request_logger, error_logger = setup_flask_logger(app, '/path/to/project')
    """
    from flask import request, g
    
    # Create different loggers for different purposes
    app_logger = setup_logger(root_dir, 'flask_app', level='INFO')
    request_logger = setup_logger(root_dir, 'flask_requests', level='INFO', console_level='WARNING')
    error_logger = setup_logger(root_dir, 'flask_errors', level='WARNING')
    
    # Disable Flask's default logger
    app.logger.handlers = []
    app.logger.propagate = False
    
    @app.before_request
    def log_request_start():
        """Log incoming request and start timer."""
        g.start_time = time.time()
        request_logger.info(
            f"Request started: {request.method} {request.path} | "
            f"IP: {request.remote_addr} | "
            f"User-Agent: {request.user_agent.string[:100]}"
        )
    
    @app.after_request
    def log_request_end(response):
        """Log response and duration."""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            request_logger.info(
                f"Request completed: {request.method} {request.path} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
        return response
    
    @app.errorhandler(Exception)
    def log_exception(error):
        """Log unhandled exceptions."""
        error_logger.exception(
            f"Unhandled exception in {request.method} {request.path}: {error}"
        )
        # Re-raise the exception to let Flask handle it
        raise
    
    # Log application startup
    app_logger.info(f"Flask application '{app.name}' started in {app.config.get('ENV', 'development')} mode")
    
    return app_logger, request_logger, error_logger


# Convenience function for quick setup
def quick_setup(project_name: str = "app") -> logging.Logger:
    """
    Quick setup with sensible defaults.
    
    Args:
        project_name: Name of the project/logger
    
    Returns:
        Configured logger instance
    
    Example:
        from api.utils.logging_config import quick_setup
        logger = quick_setup('my_project')
        logger.info('Quick setup complete')
    """
    # Use current working directory as root
    root_dir = str(Path.cwd())
    return setup_logger(root_dir, project_name, level='INFO')


# Specialized Logger Setup Functions
def setup_json_logger(root_dir: str, logging_name: str,
                     level: str = "INFO",
                     console_output: bool = True) -> logging.Logger:
    """
    Set up a logger with JSON formatted output.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Name of the logger
        level: Logging level
        console_output: Whether to also output to console
    
    Returns:
        Logger configured for JSON output
    """
    # Use base setup function for common setup
    log_dir, logger, level_upper = _setup_base_logger(root_dir, f"{logging_name}_json", level)
    
    # If logger already has handlers, return it
    if logger.handlers:
        return logger
    
    # JSON file handler
    log_file = log_dir / f'{logging_name}_json.log'
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),
        maxBytes=20 * 1024 * 1024,  # 20MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS[level_upper])
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)
    
    # Optional console handler with colored output
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    logger.info(f"JSON logger '{logging_name}' initialized", extra={'log_file': str(log_file.absolute())})
    
    return logger


def setup_colored_logger(root_dir: str, logging_name: str,
                        level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with colored console output.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Name of the logger
        level: Logging level
    
    Returns:
        Logger with colored output
    """
    log_dir = Path(root_dir) / 'logging_info'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(f"{logging_name}_colored")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVELS[level.upper()])
    logger.propagate = False
    
    # File handler with detailed format
    log_file = log_dir / f'{logging_name}.log'
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS[level.upper()])
    detailed_formatter = DetailedFormatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Colored console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVELS[level.upper()])
    colored_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)
    
    return logger


def setup_compact_logger(root_dir: str, logging_name: str,
                        level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with compact output format.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Name of the logger
        level: Logging level
    
    Returns:
        Logger with compact format
    """
    log_dir = Path(root_dir) / 'logging_info'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(f"{logging_name}_compact")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVELS[level.upper()])
    logger.propagate = False
    
    # Compact file handler
    log_file = log_dir / f'{logging_name}_compact.log'
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS[level.upper()])
    file_handler.setFormatter(CompactFormatter())
    logger.addHandler(file_handler)
    
    # Compact console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVELS[level.upper()])
    console_handler.setFormatter(CompactFormatter())
    logger.addHandler(console_handler)
    
    return logger


def setup_multi_logger(root_dir: str, logging_name: str,
                      styles: list = None) -> Dict[str, logging.Logger]:
    """
    Set up multiple loggers with different styles.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Base name for loggers
        styles: List of styles to create ('json', 'colored', 'compact', 'standard')
    
    Returns:
        Dictionary of logger instances by style
    """
    if styles is None:
        styles = ['standard', 'json', 'colored']
    
    loggers = {}
    
    for style in styles:
        if style == 'json':
            loggers['json'] = setup_json_logger(root_dir, logging_name)
        elif style == 'colored':
            loggers['colored'] = setup_colored_logger(root_dir, logging_name)
        elif style == 'compact':
            loggers['compact'] = setup_compact_logger(root_dir, logging_name)
        else:  # standard
            loggers['standard'] = setup_logger(root_dir, f"{logging_name}_{style}")
    
    return loggers


# Decorators for logging
def log_execution_time(logger: logging.Logger = None):
    """
    Decorator to log function execution time.
    
    Args:
        logger: Logger instance to use (if None, creates a default one)
    
    Example:
        @log_execution_time(logger)
        def my_function():
            time.sleep(1)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                if 'timing' not in _decorator_loggers:
                    _decorator_loggers['timing'] = quick_setup('timing')
                logger = _decorator_loggers['timing']
            
            start_time = time.time()
            func_name = func.__name__
            
            logger.debug(f"Starting execution of '{func_name}'")
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(
                    f"'{func_name}' completed successfully",
                    extra={'execution_time': f"{elapsed:.3f}s", 'status': 'success'}
                )
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"'{func_name}' failed",
                    extra={'execution_time': f"{elapsed:.3f}s", 'status': 'error', 'error': str(e)}
                )
                raise
        
        return wrapper
    return decorator


def log_function_calls(logger: logging.Logger = None, log_args: bool = False, log_result: bool = False):
    """
    Decorator to log function calls with optional argument and result logging.
    
    Args:
        logger: Logger instance to use
        log_args: Whether to log function arguments
        log_result: Whether to log function result
    
    Example:
        @log_function_calls(logger, log_args=True, log_result=True)
        def calculate(x, y):
            return x + y
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                if 'function_calls' not in _decorator_loggers:
                    _decorator_loggers['function_calls'] = quick_setup('function_calls')
                logger = _decorator_loggers['function_calls']
            
            func_name = func.__name__
            
            # Log function call
            log_msg = f"Calling '{func_name}'"
            extra = {'function': func_name}
            
            if log_args:
                extra['args'] = args
                extra['kwargs'] = kwargs
                log_msg += f" with args={args}, kwargs={kwargs}"
            
            logger.debug(log_msg, extra=extra)
            
            try:
                result = func(*args, **kwargs)
                
                if log_result:
                    logger.debug(
                        f"'{func_name}' returned: {result}",
                        extra={'function': func_name, 'result': result}
                    )
                
                return result
            except Exception as e:
                logger.exception(
                    f"'{func_name}' raised an exception",
                    extra={'function': func_name, 'exception': str(e)}
                )
                raise
        
        return wrapper
    return decorator


def log_exceptions(logger: logging.Logger = None, reraise: bool = True):
    """
    Decorator to log exceptions raised by a function.
    
    Args:
        logger: Logger instance to use
        reraise: Whether to re-raise the exception after logging
    
    Example:
        @log_exceptions(logger)
        def risky_function():
            raise ValueError("Something went wrong")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                if 'exceptions' not in _decorator_loggers:
                    _decorator_loggers['exceptions'] = quick_setup('exceptions')
                logger = _decorator_loggers['exceptions']
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(
                    f"Exception in '{func.__name__}'",
                    extra={
                        'function': func.__name__,
                        'exception_type': type(e).__name__,
                        'exception_message': str(e),
                        'traceback': traceback.format_exc()
                    }
                )
                if reraise:
                    raise
                return None
        
        return wrapper
    return decorator


# Context managers for logging
class LogContext:
    """
    Context manager for temporary logging context.
    
    Example:
        with LogContext('my_operation', logger) as ctx:
            ctx.log.info('Doing something')
            # ... operation code ...
    """
    
    def __init__(self, context_name: str, logger: Optional[logging.Logger] = None):
        self.context_name = context_name
        self.logger = logger or quick_setup('context')
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Entering context: {self.context_name}")
        self.log = self.logger  # Provide direct access to logger
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(
                f"Exiting context: {self.context_name}",
                extra={'duration': f"{elapsed:.3f}s", 'status': 'success'}
            )
        else:
            self.logger.error(
                f"Context {self.context_name} failed",
                extra={
                    'duration': f"{elapsed:.3f}s",
                    'status': 'error',
                    'exception_type': exc_type.__name__,
                    'exception': str(exc_val)
                }
            )
        
        return False  # Don't suppress exceptions


# Utility functions
def setup_rotating_logger(root_dir: str, logging_name: str,
                         when: str = "midnight",
                         interval: int = 1,
                         backup_count: int = 7,
                         level: str = "INFO") -> logging.Logger:
    """
    Set up a time-based rotating logger.
    
    Args:
        root_dir: Root directory for log files
        logging_name: Name of the logger
        when: When to rotate ('S', 'M', 'H', 'D', 'midnight')
        interval: Rotation interval
        backup_count: Number of backup files to keep
        level: Logging level
    
    Returns:
        Time-rotating logger instance
    """
    log_dir = Path(root_dir) / 'logging_info'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(f"{logging_name}_rotating")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVELS[level.upper()])
    logger.propagate = False
    
    # Time-based rotating file handler
    log_file = log_dir / f'{logging_name}_rotating.log'
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(log_file),
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS[level.upper()])
    
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger_stats(logger_name: str) -> Dict[str, Any]:
    """
    Get statistics about a logger.
    
    Args:
        logger_name: Name of the logger
    
    Returns:
        Dictionary with logger statistics
    """
    logger = logging.getLogger(logger_name)
    
    stats = {
        'name': logger.name,
        'level': logging.getLevelName(logger.level),
        'handlers_count': len(logger.handlers),
        'handlers': [],
        'propagate': logger.propagate,
        'disabled': logger.disabled
    }
    
    for handler in logger.handlers:
        handler_info = {
            'type': type(handler).__name__,
            'level': logging.getLevelName(handler.level),
        }
        
        if hasattr(handler, 'baseFilename'):
            handler_info['file'] = handler.baseFilename
        
        if hasattr(handler, 'maxBytes'):
            handler_info['max_bytes'] = handler.maxBytes
            
        if hasattr(handler, 'backupCount'):
            handler_info['backup_count'] = handler.backupCount
        
        stats['handlers'].append(handler_info)
    
    return stats


# ============================================================================
# USAGE EXAMPLES
# ============================================================================
"""
Comprehensive examples showing how to use the logging configuration module.

Example 1: Basic Setup
----------------------
from api.utils.logging_config import setup_logger

# Create a standard logger
logger = setup_logger('/path/to/project', 'my_app')
logger.info('Application started')
logger.warning('This is a warning')
logger.error('An error occurred', extra={'error_code': 500})


Example 2: JSON Logger for Structured Logging
----------------------------------------------
from api.utils.logging_config import setup_json_logger

# JSON logger for API logs (great for log aggregation services)
json_logger = setup_json_logger('/path/to/project', 'api_logs')

# Log with extra fields
json_logger.info('User login', extra={
    'user_id': 12345,
    'ip_address': '192.168.1.100',
    'user_agent': 'Mozilla/5.0...',
    'session_id': 'abc123'
})

# The output will be in JSON format:
# {"timestamp": "2024-01-20T10:30:45", "level": "INFO", "message": "User login", 
#  "user_id": 12345, "ip_address": "192.168.1.100", ...}


Example 3: Colored Logger for Development
------------------------------------------
from api.utils.logging_config import setup_colored_logger

# Colored output for better visibility during development
dev_logger = setup_colored_logger('/path/to/project', 'development')
dev_logger.debug('Debug message')  # Cyan
dev_logger.info('Info message')    # Green
dev_logger.warning('Warning')      # Yellow
dev_logger.error('Error occurred') # Red


Example 4: Flask Integration
-----------------------------
from flask import Flask
from api.utils.logging_config import setup_flask_logger

app = Flask(__name__)

# Set up Flask logging (creates 3 specialized loggers)
app_logger, request_logger, error_logger = setup_flask_logger(app, '/path/to/project')

@app.route('/api/data')
def get_data():
    app_logger.info('Fetching data from database')
    # Your route logic here
    return {'status': 'success'}

# Requests and responses are automatically logged


Example 5: Using Decorators
----------------------------
from api.utils.logging_config import (
    setup_logger,
    log_execution_time,
    log_function_calls,
    log_exceptions
)

logger = setup_logger('/path/to/project', 'my_service')

# Log execution time
@log_execution_time(logger)
def process_data(data):
    # Some time-consuming operation
    import time
    time.sleep(2)
    return len(data)

# Log function calls with arguments and results
@log_function_calls(logger, log_args=True, log_result=True)
def calculate(x, y, operation='add'):
    if operation == 'add':
        return x + y
    elif operation == 'multiply':
        return x * y

# Automatically log exceptions
@log_exceptions(logger)
def risky_operation(value):
    if value < 0:
        raise ValueError('Value must be positive')
    return value ** 2

# Usage
result = process_data([1, 2, 3])  # Logs: Function executed in 2.001s
calc_result = calculate(5, 3, operation='multiply')  # Logs args and result: 15
try:
    risky_operation(-5)  # Exception will be logged with full traceback
except ValueError:
    pass


Example 6: Context Manager for Operations
------------------------------------------
from api.utils.logging_config import LogContext, setup_logger

logger = setup_logger('/path/to/project', 'operations')

# Use context manager for timed operations
with LogContext('database_migration', logger) as ctx:
    ctx.log.info('Starting migration of users table')
    # ... perform migration ...
    ctx.log.info('Migration completed')
# Automatically logs entry, exit, and duration


Example 7: Multiple Logger Styles
----------------------------------
from api.utils.logging_config import setup_multi_logger

# Create multiple loggers with different formats
loggers = setup_multi_logger(
    '/path/to/project',
    'my_app',
    styles=['standard', 'json', 'colored', 'compact']
)

# Use different loggers for different purposes
loggers['standard'].info('Regular log message')
loggers['json'].info('API request', extra={'endpoint': '/api/users'})
loggers['colored'].warning('Warning with colors')
loggers['compact'].debug('Compact format')


Example 8: Time-Based Rotating Logger
--------------------------------------
from api.utils.logging_config import setup_rotating_logger

# Rotate logs daily at midnight
daily_logger = setup_rotating_logger(
    '/path/to/project',
    'daily_logs',
    when='midnight',
    backup_count=30  # Keep 30 days of logs
)

# Rotate logs every hour
hourly_logger = setup_rotating_logger(
    '/path/to/project',
    'hourly_logs',
    when='H',
    interval=1,
    backup_count=24  # Keep 24 hours of logs
)


Example 9: Custom Log Levels and Formats
-----------------------------------------
from api.utils.logging_config import setup_logger

# Custom format
custom_logger = setup_logger(
    '/path/to/project',
    'custom',
    level='DEBUG',
    console_level='WARNING',  # Console only shows warnings and above
    log_format='%(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
)


Example 10: Real Flask Application Example
-------------------------------------------
# In your index.py or app.py
from flask import Flask
from api.utils.logging_config import setup_json_logger, log_execution_time
import os

app = Flask(__name__)

# Get root directory
root_dir = os.path.dirname(os.path.abspath(__file__))

# Set up JSON logger for production
logger = setup_json_logger(root_dir, 'flask_app', level='INFO')

@app.route('/api/users/<int:user_id>')
@log_execution_time(logger)
def get_user(user_id):
    logger.info('Fetching user', extra={'user_id': user_id})
    # Database operation here
    user = {'id': user_id, 'name': 'John Doe'}
    logger.info('User fetched successfully', extra={'user': user})
    return user


Example 11: Scheduler/Background Task Logging
----------------------------------------------
from api.utils.logging_config import setup_logger, LogContext
from pathlib import Path

# For background tasks
task_logger = setup_logger(
    str(Path.cwd()),
    'scheduler_tasks',
    level='INFO'
)

def scheduled_task():
    with LogContext('data_sync_task', task_logger) as ctx:
        ctx.log.info('Starting data synchronization')
        
        try:
            # Your task logic
            records_processed = 1000
            ctx.log.info(f'Processed {records_processed} records')
            
        except Exception as e:
            ctx.log.error(f'Task failed: {e}')
            raise


Example 12: Getting Logger Statistics
--------------------------------------
from api.utils.logging_config import setup_logger, get_logger_stats

# Create a logger
logger = setup_logger('/path/to/project', 'my_app')

# Get statistics
stats = get_logger_stats('my_app')
print(f"Logger: {stats['name']}")
print(f"Level: {stats['level']}")
print(f"Number of handlers: {stats['handlers_count']}")
for handler in stats['handlers']:
    print(f"  - {handler['type']}: {handler.get('file', 'console')}")


Example 13: Quick Setup for Scripts
------------------------------------
from api.utils.logging_config import quick_setup

# Quick setup with defaults (uses current directory)
logger = quick_setup('my_script')
logger.info('Script started')
logger.error('Something went wrong!')


Example 14: Cleanup Loggers
----------------------------
from api.utils.logging_config import setup_logger, cleanup_logger

# Create logger
logger = setup_logger('/path/to/project', 'temporary')
logger.info('Doing some work')

# Clean up when done (closes file handlers)
cleanup_logger('temporary')
"""