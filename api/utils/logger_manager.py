from loguru import logger
import sys
from pathlib import Path
from typing import Optional, Any, Callable
import builtins
import json
from datetime import datetime
from functools import wraps


class LoggerManager:
    """
    A comprehensive logging manager built on top of loguru.

    Basic usage:
        >>> import sys
        >>> from io import StringIO
        >>> # Redirect stdout to capture output for testing
        >>> old_stdout = sys.stdout
        >>> sys.stdout = StringIO()
        >>>
        >>> log_manager = LoggerManager(mode="dev")
        >>> log = log_manager.get_logger()
        >>> # Restore stdout
        >>> sys.stdout = old_stdout

    With custom configuration:
        >>> log_manager = LoggerManager(
        ...     log_file_path="logs/app.log",
        ...     level="INFO",
        ...     console_level="WARNING",
        ...     json_format=True
        ... )
    """

    def __init__(self, *,
                 log_name: str = "app",
                 log_file_path: str = "logs/app.log",
                 level: str = "DEBUG",
                 retention: str = "7 days",
                 rotation: str = "500 MB",
                 json_format: bool = False,
                 mode: str = "dev",  # or "prod"
                 console_level: Optional[str] = None,  # Override console output level
                 enable_print_redirect: bool = False,
                 enable_exception_logging: bool = True,
                 custom_format: Optional[str] = None,
                 colorize: Optional[bool] = None,  # None means True
                 backtrace: Optional[bool] = None,
                 diagnose: Optional[bool] = None,
                 catch_exceptions: bool = True,
                 extra_handlers: Optional[list] = None,
                 filter_func: Optional[Callable] = None  # Custom filter function
                 ):
        self.log_name = log_name
        self.log_file_path = Path(log_file_path)
        self.level = level.upper()
        self.retention = retention
        self.rotation = rotation
        self.json_format = json_format
        self.mode = mode.lower()

        # Pre-compute mode flags
        self.is_dev = self.mode == "dev"
        self.is_prod = self.mode == "prod"

        # Console level logic: explicit > mode-based default > file level
        self.console_level = (
            console_level.upper() if console_level else
            ("INFO" if self.is_dev else self.level)
        )

        self.enable_print_redirect = enable_print_redirect
        self.enable_exception_logging = enable_exception_logging
        self.custom_format = custom_format

        # Console output is plain text, no colors
        self.colorize = colorize if colorize is not None else False

        # Dev mode defaults for debugging features
        self.backtrace = backtrace if backtrace is not None else self.is_dev
        self.diagnose = diagnose if diagnose is not None else self.is_dev

        self.catch_exceptions = catch_exceptions
        self.extra_handlers = extra_handlers or []
        self.filter_func = filter_func

        # Store original print function
        self._original_print = builtins.print
        self._print_redirected = False

        # Store handler IDs for cleanup
        self._handler_ids = []

        self._setup_logger()

    def _setup_logger(self):
        """Configure the logger with all specified settings."""
        # Remove default handlers
        logger.remove()

        # Console output - plain format for both dev and prod (no colors)
        console_format = "{time:YYYY-MM-DD HH:mm:ss} | {level:<5} | {message}"

        handler_id = logger.add(
            sys.stdout,
            level=self.console_level,
            format=console_format,
            colorize=False,  # No colors for console output
            backtrace=self.backtrace,
            diagnose=self.diagnose,
            filter=self.filter_func
        )
        self._handler_ids.append(handler_id)

        # Create log directory if it doesn't exist
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # File logging format - simplified
        if self.json_format:
            # Use serialize=True instead of custom formatter for JSON
            log_format = "{message}"
            file_serialize = True
        else:
            # Simplified format for file output
            log_format = self.custom_format or (
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level:<5} | "
                "{function}:{line} | "
                "{message}"
            )
            file_serialize = False

        # Add file handler
        handler_id = logger.add(
            sink=self.log_file_path,
            level=self.level,
            rotation=self.rotation,
            retention=self.retention,
            format=log_format,
            backtrace=self.backtrace,
            diagnose=self.diagnose,
            enqueue=True,  # Thread-safe
            serialize=file_serialize,  # Use JSON serialization if json_format is True
            filter=self.filter_func
        )
        self._handler_ids.append(handler_id)

        # Add extra handlers
        for handler in self.extra_handlers:
            if 'filter' not in handler and self.filter_func:
                handler['filter'] = self.filter_func
            handler_id = logger.add(**handler)
            self._handler_ids.append(handler_id)

        # Redirect print to logger if enabled
        if self.enable_print_redirect:
            self._redirect_print()

        # Set up exception logging
        if self.enable_exception_logging:
            self._setup_exception_logging()


    def _redirect_print(self):
        """Redirect print statements to logger."""
        if self._print_redirected:
            return

        def custom_print(*args, **kwargs):
            message = " ".join(map(str, args))
            logger.opt(depth=1).info(f"[PRINT] {message}")

        builtins.print = custom_print
        self._print_redirected = True

    def restore_print(self):
        """Restore original print function."""
        if self._print_redirected:
            builtins.print = self._original_print
            self._print_redirected = False

    def _setup_exception_logging(self):
        """Set up automatic exception logging."""
        if self.catch_exceptions:
            @logger.catch(reraise=True)
            def wrapper(func):
                return func

            self.exception_handler = wrapper

    def add_handler(self, **kwargs) -> int:
        """
        Add a custom handler to the logger.

        Returns:
            Handler ID that can be used to remove the handler later
        """
        if 'filter' not in kwargs and self.filter_func:
            kwargs['filter'] = self.filter_func
        handler_id = logger.add(**kwargs)
        self._handler_ids.append(handler_id)
        return handler_id

    def remove_handler(self, handler_id: int):
        """Remove a handler by ID."""
        logger.remove(handler_id)
        if handler_id in self._handler_ids:
            self._handler_ids.remove(handler_id)

    def bind(self, **kwargs):
        """Bind contextual data to logger."""
        return logger.bind(**kwargs)

    def contextualize(self, **kwargs):
        """Context manager for temporary contextual data."""
        return logger.contextualize(**kwargs)

    def configure(self, **kwargs):
        """Configure logger with additional options."""
        logger.configure(**kwargs)

    def get_logger(self):
        """Get the configured logger instance."""
        return logger

    def flush(self):
        """
        Force flush all log handlers.
        Useful for ensuring all logs are written before shutdown.
        """
        for handler_id in self._handler_ids:
            try:
                # Loguru doesn't have a direct flush method, but we can complete the queue
                logger.complete()
            except Exception:
                pass

    def log_performance(self, include_args: bool = False, log_exceptions: bool = True) -> Callable:
        """
        Decorator to log function performance with exception handling.

        Args:
            include_args: Whether to log function arguments
            log_exceptions: Whether to log exceptions if they occur

        Usage:
            @log_manager.log_performance()
            def slow_function(x, y):
                import time
                time.sleep(0.1)
                return x + y
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                func_name = func.__name__
                start_time = datetime.now()

                # Prepare argument string if needed
                arg_str = ""
                if include_args:
                    arg_list = [repr(arg) for arg in args]
                    kwarg_list = [f"{k}={repr(v)}" for k, v in kwargs.items()]
                    arg_str = f" with args: ({', '.join(arg_list + kwarg_list)})"

                try:
                    result = func(*args, **kwargs)
                    duration = (datetime.now() - start_time).total_seconds()
                    logger.info(f"Function '{func_name}'{arg_str} executed successfully in {duration:.3f} seconds")
                    return result
                except Exception as e:
                    duration = (datetime.now() - start_time).total_seconds()
                    if log_exceptions:
                        logger.exception(f"Function '{func_name}'{arg_str} failed after {duration:.3f} seconds")
                    raise

            return wrapper

        return decorator

    def create_child_logger(self, name: str) -> Any:
        """Create a child logger with a specific name."""
        return logger.bind(logger_name=name)

    def set_filter(self, filter_func: Optional[Callable]):
        """
        Set or update the filter function for all handlers.

        Args:
            filter_func: Function that takes a record and returns bool

        Usage:
            def my_filter(record):
                return "password" not in record["message"].lower()
            log_manager.set_filter(my_filter)
        """
        self.filter_func = filter_func
        # Re-setup logger with new filter
        self.cleanup()
        self._setup_logger()

    def cleanup(self):
        """Clean up all handlers and restore print if needed."""
        # Remove all our handlers
        for handler_id in self._handler_ids[:]:  # Copy list to avoid modification during iteration
            try:
                logger.remove(handler_id)
            except ValueError:
                pass  # Handler already removed
        self._handler_ids.clear()

        # Restore print
        self.restore_print()

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up on exit."""
        self.flush()
        if self.enable_print_redirect:
            self.restore_print()
        return False

    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            self.cleanup()
        except Exception:
            pass  # Ignore errors during cleanup


# Example configurations for common use cases
class LogConfigs:
    """Pre-configured logging setups for common scenarios."""

    @staticmethod
    def development():
        """Development configuration with verbose logging."""
        return LoggerManager(
            log_name="afm_data_viewer_dev",
            log_file_path="logs/afm_data_viewer_dev.log",
            level="DEBUG",
            console_level="INFO",  # Less verbose console output
            retention="3 days",
            rotation="100 MB",
            mode="dev",
            enable_print_redirect=True
        )

    @staticmethod
    def production():
        """Production configuration with JSON formatting for files."""
        return LoggerManager(
            log_name="afm_data_viewer_prod",
            log_file_path="logs/afm_data_viewer_prod.log",
            level="INFO",
            console_level="WARNING",  # Only warnings and errors to console
            retention="30 days",
            rotation="1 GB",
            mode="prod",
            json_format=True,  # JSON for file logs
            backtrace=True,  # Include backtrace for debugging
            diagnose=False  # Don't include local variables in prod
        )

    @staticmethod
    def testing():
        """Testing configuration with full debug info."""
        return LoggerManager(
            log_name="afm_data_viewer_test",
            log_file_path="logs/afm_data_viewer_test.log",
            level="DEBUG",
            console_level="DEBUG",
            retention="1 day",
            rotation="50 MB",
            mode="dev"
        )

    @staticmethod
    def minimal():
        """Minimal configuration for scripts and small apps."""
        return LoggerManager(
            log_name="afm_data_viewer_minimal",
            log_file_path="logs/afm_data_viewer.log",
            level="INFO",
            retention="7 days",
            rotation="10 MB",
            mode="prod"
        )


# Example usage
if __name__ == "__main__":
    # Basic usage with context manager
    with LoggerManager(mode="dev", enable_print_redirect=True) as log_manager:
        log = log_manager.get_logger()

        # Basic logging
        log.debug("This is a debug message")
        log.info("This is an info message")
        log.warning("This is a warning")
        log.error("This is an error")

        # Print redirection
        print("This print statement is redirected to logs")

        # Logging with extra context
        log.bind(user_id=123, request_id="abc123").info("User action logged")

        # Using context manager for temporary context
        with log_manager.contextualize(transaction_id="xyz789"):
            log.info("Processing transaction")
            log.info("Transaction completed")


        # Performance logging with exception handling
        @log_manager.log_performance(include_args=True, log_exceptions=True)
        def divide_numbers(a, b):
            return a / b


        # This will log performance
        result = divide_numbers(10, 2)

        # This will log the exception
        try:
            result = divide_numbers(10, 0)
        except ZeroDivisionError:
            pass


        # Filter example
        def no_password_filter(record):
            return "password" not in record["message"].lower()


        log_manager.set_filter(no_password_filter)
        log.info("User logged in with password: secret123")  # This won't be logged
        log.info("User logged in successfully")  # This will be logged

        # Force flush before critical operation
        log_manager.flush()

    # Using pre-configured setups
    dev_logger = LogConfigs.development()
    prod_logger = LogConfigs.production()

    # Minimal setup for scripts
    with LogConfigs.minimal() as log_manager:
        log = log_manager.get_logger()
        log.info("Script completed successfully")