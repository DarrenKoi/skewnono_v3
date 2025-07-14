"""
Extended Usage Examples for LogManager
=====================================

This file contains comprehensive examples to help team members
effectively use the LogManager in various scenarios.
"""

from loguru import logger
from pathlib import Path
import asyncio
import time
from contextlib import contextmanager
import requests
from logger_manager import LoggerManager, LogConfigs


# =============================================================================
# 1. BASIC USAGE PATTERNS
# =============================================================================

def basic_logging_example():
    """Example 1: Basic logging with different levels"""
    log_manager = LoggerManager(mode="dev")
    log = log_manager.get_logger()

    # Different log levels
    log.trace("Detailed trace information")
    log.debug("Debug information for developers")
    log.info("General information about program execution")
    log.success("Operation completed successfully!")  # Special loguru level
    log.warning("Warning: Resource usage is high")
    log.error("Error occurred but program can continue")
    log.critical("Critical error - immediate attention needed")

    # Cleanup
    log_manager.cleanup()


# =============================================================================
# 2. STRUCTURED LOGGING WITH CONTEXT
# =============================================================================

def structured_logging_example():
    """Example 2: Adding structured context to logs"""
    log_manager = LoggerManager(
        mode="prod",
        json_format=True,  # Enable JSON format for structured logging
        log_file_path="logs/structured.log"
    )
    log = log_manager.get_logger()

    # Method 1: Bind permanent context
    contextualized_logger = log.bind(
        service="user-api",
        version="2.1.0",
        environment="production"
    )

    contextualized_logger.info("Service started")

    # Method 2: Temporary context with context manager
    with log_manager.contextualize(request_id="req-12345", user_id="user-789"):
        log.info("Processing user request")
        log.info("Request validation passed")
        log.info("Request completed")

    # Context is automatically removed after the with block
    log.info("Back to normal logging")

    log_manager.cleanup()


# =============================================================================
# 3. LOGGING IN WEB APPLICATIONS (Flask/FastAPI example)
# =============================================================================

def web_app_logging_example():
    """Example 3: Logging in web applications with request tracking"""
    from uuid import uuid4

    log_manager = LoggerManager(
        log_name="web_app",
        mode="prod",
        json_format=True,
        console_level="INFO",
        level="DEBUG"
    )
    log = log_manager.get_logger()

    # Simulate a request handler
    def handle_request(endpoint: str, method: str, user_id: str = None):
        request_id = str(uuid4())

        # Create request-specific logger
        request_logger = log.bind(
            request_id=request_id,
            endpoint=endpoint,
            method=method,
            user_id=user_id
        )

        request_logger.info("Request started")

        try:
            # Simulate processing
            time.sleep(0.1)
            request_logger.info("Processing business logic")

            # Simulate database query
            request_logger.debug("Executing database query",
                                 query="SELECT * FROM users WHERE id = ?",
                                 params=[user_id])

            request_logger.success("Request completed",
                                   status_code=200,
                                   response_time_ms=105)
        except Exception as e:
            request_logger.exception("Request failed")
            raise

    # Example usage
    handle_request("/api/users/profile", "GET", "user-123")
    handle_request("/api/users/update", "POST", "user-456")

    log_manager.cleanup()


# =============================================================================
# 4. ASYNC LOGGING WITH COROUTINES
# =============================================================================

async def async_logging_example():
    """Example 4: Logging in async applications"""
    log_manager = LoggerManager(
        log_name="async_app",
        mode="dev",
        enable_print_redirect=True
    )
    log = log_manager.get_logger()

    async def fetch_data(url: str, task_id: int):
        task_logger = log.bind(task_id=task_id, url=url)
        task_logger.info("Starting async fetch")

        try:
            # Simulate async operation
            await asyncio.sleep(0.5)
            task_logger.success("Data fetched successfully")
            return f"Data from {url}"
        except Exception as e:
            task_logger.exception("Failed to fetch data")
            raise

    # Run multiple async tasks
    urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
    tasks = [fetch_data(url, i) for i, url in enumerate(urls)]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    log.info(f"Completed {len(results)} async operations")

    log_manager.cleanup()


# =============================================================================
# 5. PERFORMANCE MONITORING AND PROFILING
# =============================================================================

def performance_monitoring_example():
    """Example 5: Using performance decorators and monitoring"""
    log_manager = LoggerManager(mode="dev")
    log = log_manager.get_logger()

    # Using the performance decorator
    @log_manager.log_performance(include_args=True)
    def process_batch(batch_size: int, processing_type: str):
        """Simulate batch processing"""
        log.info(f"Processing {batch_size} items")
        time.sleep(0.1 * batch_size / 1000)  # Simulate work
        return f"Processed {batch_size} items"

    # Manual performance tracking
    def manual_performance_tracking():
        with log.contextualize(operation="data_import"):
            start_time = time.time()
            log.info("Starting data import")

            # Simulate steps
            for i in range(5):
                step_start = time.time()
                time.sleep(0.1)
                step_duration = time.time() - step_start
                log.debug(f"Step {i + 1} completed", duration_seconds=step_duration)

            total_duration = time.time() - start_time
            log.success("Data import completed",
                        total_duration_seconds=total_duration,
                        records_processed=5000)

    # Execute examples
    process_batch(1000, "standard")
    process_batch(5000, "bulk")
    manual_performance_tracking()

    log_manager.cleanup()


# =============================================================================
# 6. ERROR HANDLING AND EXCEPTION LOGGING
# =============================================================================

def error_handling_example():
    """Example 6: Comprehensive error handling and logging"""
    log_manager = LoggerManager(
        mode="dev",
        enable_exception_logging=True,
        backtrace=True,
        diagnose=True
    )
    log = log_manager.get_logger()

    class BusinessError(Exception):
        """Custom business logic exception"""
        pass

    def risky_operation(value: int):
        """Simulate an operation that might fail"""
        log.debug(f"Starting risky operation with value: {value}")

        if value < 0:
            raise ValueError("Value cannot be negative")
        elif value == 0:
            raise BusinessError("Business rule violation: value cannot be zero")
        elif value > 100:
            log.warning("Value is unusually high", value=value)

        result = 100 / value
        log.info("Operation successful", result=result)
        return result

    # Test different scenarios
    test_values = [50, 150, 0, -10, 5]

    for val in test_values:
        try:
            result = risky_operation(val)
            log.success(f"Processed value {val} successfully")
        except BusinessError as e:
            log.error(f"Business error for value {val}: {e}")
        except ValueError as e:
            log.error(f"Validation error for value {val}: {e}")
        except Exception as e:
            log.exception(f"Unexpected error for value {val}")

    log_manager.cleanup()


# =============================================================================
# 7. LOG FILTERING AND SENSITIVE DATA
# =============================================================================

def log_filtering_example():
    """Example 7: Filtering sensitive information from logs"""

    # Define custom filters
    def security_filter(record):
        """Filter out sensitive information"""
        message = record["message"]

        # List of sensitive keywords
        sensitive_keywords = ["password", "token", "secret", "api_key", "ssn"]

        # Check if message contains sensitive data
        for keyword in sensitive_keywords:
            if keyword.lower() in message.lower():
                return False  # Don't log this message

        return True  # Log this message

    def level_and_module_filter(record):
        """Complex filter based on level and module"""
        # Always log warnings and above
        if record["level"].no >= 30:  # WARNING = 30
            return True

        # For lower levels, only log from specific modules
        allowed_modules = ["important_module", "critical_service"]
        return record["module"] in allowed_modules

    # Create logger with filter
    log_manager = LogManager(
        mode="prod",
        filter_func=security_filter
    )
    log = log_manager.get_logger()

    # Test filtering
    log.info("User logged in successfully")  # This will be logged
    log.info("User password is: secret123")  # This will be filtered out
    log.info("API token: abcd1234")  # This will be filtered out
    log.warning("Authentication failed")  # This will be logged

    # Change filter at runtime
    log_manager.set_filter(level_and_module_filter)
    log.info("This might be filtered based on module")

    log_manager.cleanup()


# =============================================================================
# 8. MULTI-HANDLER LOGGING (File, Console, External Services)
# =============================================================================

def multi_handler_example():
    """Example 8: Logging to multiple destinations"""

    # Custom handler for critical errors
    def email_handler(message):
        """Simulate sending email for critical errors"""
        record = message.record
        if record["level"].name == "CRITICAL":
            print(f"[EMAIL ALERT] Critical error: {record['message']}")

    # Create logger with multiple handlers
    log_manager = LoggerManager(
        mode="prod",
        log_file_path="logs/app.log",
        console_level="INFO",
        level="DEBUG",
        extra_handlers=[
            {
                "sink": "logs/errors.log",
                "level": "ERROR",
                "rotation": "100 MB",
                "retention": "30 days",
                "format": "{time} | {level} | {message}"
            },
            {
                "sink": "logs/critical.log",
                "level": "CRITICAL",
                "format": "{time} | CRITICAL ALERT | {message}",
                "serialize": True
            },
            {
                "sink": email_handler,
                "level": "CRITICAL"
            }
        ]
    )
    log = log_manager.get_logger()

    # Test different log levels
    log.debug("Debug information")
    log.info("Application started")
    log.warning("Memory usage high")
    log.error("Failed to connect to database")
    log.critical("System is out of memory!")

    log_manager.cleanup()


# =============================================================================
# 9. LOGGING IN CLASS-BASED APPLICATIONS
# =============================================================================

class DatabaseService:
    """Example 9: Logging in class-based applications"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.log_manager = LoggerManager(
            log_name="database_service",
            log_file_path="logs/database.log",
            mode="prod"
        )
        self.log = self.log_manager.get_logger().bind(
            service="DatabaseService",
            connection=connection_string.split('@')[-1]  # Hide credentials
        )
        self.log.info("DatabaseService initialized")

    def connect(self):
        """Establish database connection"""
        self.log.info("Attempting to connect to database")
        try:
            # Simulate connection
            time.sleep(0.1)
            self.log.success("Database connection established")
            return True
        except Exception as e:
            self.log.exception("Failed to connect to database")
            return False

    def execute_query(self, query: str, params: list = None):
        """Execute a database query"""
        query_logger = self.log.bind(
            query_type=query.split()[0].upper(),
            query_length=len(query)
        )

        query_logger.debug("Executing query", query=query[:100])  # Log first 100 chars

        try:
            # Simulate query execution
            time.sleep(0.05)
            query_logger.info("Query executed successfully", rows_affected=42)
            return {"status": "success", "rows": 42}
        except Exception as e:
            query_logger.exception("Query execution failed")
            raise

    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'log'):
            self.log.info("DatabaseService shutting down")
        if hasattr(self, 'log_manager'):
            self.log_manager.cleanup()


# =============================================================================
# 10. TESTING WITH LOGGING
# =============================================================================

def testing_with_logging_example():
    """Example 10: Using logging in tests"""
    import io
    import sys

    class TestLogger:
        """Helper class for capturing logs in tests"""

        def __init__(self):
            self.log_capture = io.StringIO()
            self.log_manager = LoggerManager(
                mode="test",
                level="DEBUG",
                extra_handlers=[{
                    "sink": self.log_capture,
                    "format": "{level}|{message}"
                }]
            )
            self.log = self.log_manager.get_logger()

        def get_logs(self):
            """Get captured log messages"""
            return self.log_capture.getvalue()

        def assert_log_contains(self, text: str):
            """Assert that logs contain specific text"""
            logs = self.get_logs()
            assert text in logs, f"'{text}' not found in logs:\n{logs}"

        def cleanup(self):
            self.log_manager.cleanup()
            self.log_capture.close()

    # Example test
    def test_user_service():
        test_logger = TestLogger()
        log = test_logger.log

        # Simulate service behavior
        log.info("Creating user", username="testuser")
        log.debug("Validating user data")
        log.success("User created successfully", user_id=123)

        # Verify logs
        test_logger.assert_log_contains("Creating user")
        test_logger.assert_log_contains("user_id")
        test_logger.assert_log_contains("SUCCESS")

        print("✓ Test passed!")
        test_logger.cleanup()

    test_user_service()


# =============================================================================
# 11. PRODUCTION BEST PRACTICES
# =============================================================================

def production_best_practices():
    """Example 11: Production-ready logging configuration"""

    @contextmanager
    def production_logger(service_name: str):
        """Context manager for production logging"""
        log_manager = LoggerManager(
            log_name=service_name,
            log_file_path=f"logs/{service_name}/{service_name}.log",
            mode="prod",
            level="INFO",  # Don't log DEBUG in production
            console_level="WARNING",  # Minimal console output
            json_format=True,  # Structured logs for log aggregation
            retention="30 days",
            rotation="1 GB",
            enable_exception_logging=True,
            serialize=True,  # For log parsing tools
            extra_handlers=[
                {
                    # Separate error log
                    "sink": f"logs/{service_name}/errors.log",
                    "level": "ERROR",
                    "retention": "90 days",
                    "serialize": True
                }
            ]
        )

        log = log_manager.get_logger()

        # Add service metadata
        log = log.bind(
            service=service_name,
            host=Path.cwd().name,  # Simplified, use socket.gethostname() in real app
            pid=id(log_manager),  # Simplified, use os.getpid() in real app
            version="1.0.0"
        )

        try:
            yield log
        finally:
            log.info(f"Shutting down {service_name}")
            log_manager.flush()
            log_manager.cleanup()

    # Usage
    with production_logger("payment_service") as log:
        log.info("Payment service started")

        # Simulate payment processing
        def process_payment(amount: float, currency: str, user_id: str):
            payment_log = log.bind(
                amount=amount,
                currency=currency,
                user_id=user_id,
                transaction_id=f"txn_{int(time.time())}"
            )

            payment_log.info("Processing payment")

            # Simulate validation
            if amount <= 0:
                payment_log.error("Invalid payment amount")
                return False

            # Simulate processing
            time.sleep(0.1)
            payment_log.success("Payment processed successfully")
            return True

        # Process some payments
        process_payment(99.99, "USD", "user-123")
        process_payment(-10.00, "EUR", "user-456")  # This will fail
        process_payment(49.99, "GBP", "user-789")


# =============================================================================
# 12. CUSTOM LOG FORMATS FOR DIFFERENT ENVIRONMENTS
# =============================================================================

def custom_format_example():
    """Example 12: Custom log formats for different needs"""

    # Format for developers (readable, with colors)
    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level> | "
        "<dim>{extra}</dim>"
    )

    # Format for production (parseable)
    prod_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS ZZ} "
        "level={level.name} "
        "logger={name} "
        "function={function} "
        "message=\"{message}\" "
        "{extra}"
    )

    # Format for audit logs (detailed)
    audit_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS ZZ} | "
        "AUDIT | "
        "level={level.name} | "
        "user={extra[user_id]} | "
        "action={extra[action]} | "
        "resource={extra[resource]} | "
        "result={extra[result]} | "
        "message={message}"
    )

    # Example: Development logger
    dev_logger = LoggerManager(
        mode="dev",
        custom_format=dev_format
    )
    log = dev_logger.get_logger()
    log.bind(request_id="req-123").info("Processing request")
    dev_logger.cleanup()

    # Example: Audit logger
    audit_logger = LoggerManager(
        log_name="audit",
        log_file_path="logs/audit.log",
        custom_format=audit_format,
        mode="prod"
    )
    audit_log = audit_logger.get_logger()

    # Log audit events
    audit_log.bind(
        user_id="admin-001",
        action="DELETE",
        resource="user/123",
        result="SUCCESS"
    ).warning("Administrator deleted user account")

    audit_logger.cleanup()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("Running LogManager Usage Examples...\n")

    examples = [
        ("Basic Logging", basic_logging_example),
        ("Structured Logging", structured_logging_example),
        ("Web Application Logging", web_app_logging_example),
        ("Performance Monitoring", performance_monitoring_example),
        ("Error Handling", error_handling_example),
        ("Log Filtering", log_filtering_example),
        ("Multi-Handler Logging", multi_handler_example),
        ("Testing with Logging", testing_with_logging_example),
        ("Production Best Practices", production_best_practices),
        ("Custom Formats", custom_format_example)
    ]

    for name, example_func in examples:
        print(f"\n{'=' * 60}")
        print(f"Running Example: {name}")
        print(f"{'=' * 60}")

        try:
            if asyncio.iscoroutinefunction(example_func):
                asyncio.run(example_func())
            else:
                example_func()
        except Exception as e:
            print(f"Error in {name}: {e}")

        time.sleep(0.5)  # Brief pause between examples

    # Class-based example
    print(f"\n{'=' * 60}")
    print(f"Running Example: Class-based Logging")
    print(f"{'=' * 60}")

    db_service = DatabaseService("postgresql://localhost/mydb")
    db_service.connect()
    db_service.execute_query("SELECT * FROM users WHERE active = ?", [True])
    del db_service  # Trigger cleanup

    print("\n✅ All examples completed!")