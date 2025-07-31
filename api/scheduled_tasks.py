"""
Example scheduled background tasks with proper logging.
These tasks demonstrate how to use the centralized logger in background jobs.
"""
import time
import random
from datetime import datetime
from .utils.app_logger import get_task_logger
from .utils.scheduler import add_scheduled_job

def data_sync_task():
    """Example task: Sync data from external sources"""
    logger = get_task_logger("data_sync")
    
    logger.info("Starting data synchronization...")
    
    # Simulate data sources
    data_sources = ["Database A", "API B", "File System C"]
    
    for source in data_sources:
        try:
            # Simulate processing time
            process_time = random.uniform(0.1, 0.5)
            time.sleep(process_time)
            
            # Simulate success/failure
            if random.random() > 0.9:  # 10% chance of failure
                raise Exception(f"Failed to connect to {source}")
            
            records = random.randint(100, 1000)
            logger.info(f"Synced {records} records from {source}",
                       source=source,
                       records=records,
                       duration=process_time)
            
        except Exception as e:
            logger.error(f"Error syncing from {source}: {str(e)}",
                        source=source,
                        error=str(e))
    
    logger.success("Data synchronization completed")

def cleanup_old_logs_task():
    """Example task: Clean up old log entries"""
    logger = get_task_logger("log_cleanup")
    
    logger.info("Starting log cleanup task...")
    
    # Simulate cleanup
    try:
        # Check log directory size
        log_size_mb = random.randint(50, 500)
        logger.debug(f"Current log size: {log_size_mb}MB")
        
        if log_size_mb > 200:
            # Simulate cleanup
            time.sleep(0.5)
            cleaned_mb = random.randint(50, 150)
            logger.info(f"Cleaned up {cleaned_mb}MB of old logs",
                       before_size=log_size_mb,
                       after_size=log_size_mb - cleaned_mb,
                       cleaned=cleaned_mb)
        else:
            logger.info("No cleanup needed, log size is within limits",
                       current_size=log_size_mb,
                       limit=200)
    
    except Exception as e:
        logger.exception("Error during log cleanup")
        raise

def health_check_task():
    """Example task: System health check"""
    logger = get_task_logger("health_check")
    
    logger.info("Running system health check...")
    
    # Simulate health checks
    checks = {
        "database": random.random() > 0.05,  # 95% healthy
        "redis": random.random() > 0.1,      # 90% healthy
        "disk_space": random.random() > 0.2, # 80% healthy
        "memory": random.random() > 0.15,    # 85% healthy
    }
    
    all_healthy = True
    for component, is_healthy in checks.items():
        if is_healthy:
            logger.debug(f"{component}: OK", component=component, status="healthy")
        else:
            logger.warning(f"{component}: UNHEALTHY", component=component, status="unhealthy")
            all_healthy = False
    
    if all_healthy:
        logger.success("All systems healthy")
    else:
        logger.warning("Some systems require attention",
                      failed_checks=[k for k, v in checks.items() if not v])

def generate_report_task():
    """Example task: Generate daily reports"""
    logger = get_task_logger("report_generation")
    
    logger.info("Starting report generation...")
    
    report_types = ["daily_summary", "performance_metrics", "error_analysis"]
    
    for report_type in report_types:
        try:
            logger.debug(f"Generating {report_type} report...")
            
            # Simulate report generation
            time.sleep(random.uniform(0.5, 1.5))
            
            # Simulate file creation
            file_path = f"reports/{report_type}_{datetime.now().strftime('%Y%m%d')}.pdf"
            file_size = random.randint(100, 500)
            
            logger.info(f"Generated {report_type} report",
                       report_type=report_type,
                       file_path=file_path,
                       file_size_kb=file_size)
            
        except Exception as e:
            logger.error(f"Failed to generate {report_type} report",
                        report_type=report_type,
                        error=str(e))

def register_scheduled_tasks():
    """Register all scheduled tasks with the scheduler"""
    logger = get_task_logger("task_registration")
    
    try:
        # Data sync every 5 minutes
        add_scheduled_job(
            data_sync_task,
            'interval',
            minutes=5,
            id='data_sync',
            name='Data Synchronization'
        )
        
        # Log cleanup every hour
        add_scheduled_job(
            cleanup_old_logs_task,
            'interval',
            hours=1,
            id='log_cleanup',
            name='Log Cleanup'
        )
        
        # Health check every 2 minutes
        add_scheduled_job(
            health_check_task,
            'interval',
            minutes=2,
            id='health_check',
            name='System Health Check'
        )
        
        # Daily report at 2 AM
        add_scheduled_job(
            generate_report_task,
            'cron',
            hour=2,
            minute=0,
            id='daily_report',
            name='Daily Report Generation'
        )
        
        logger.success("All scheduled tasks registered successfully")
        
    except Exception as e:
        logger.exception("Failed to register scheduled tasks")
        raise

# Function to manually test a task
def test_task_logging():
    """Test function to verify task logging works correctly"""
    logger = get_task_logger("test_task")
    
    logger.info("This is a test task")
    logger.debug("Debug information", test_data={"key": "value"})
    logger.warning("Test warning")
    
    try:
        raise ValueError("Test error")
    except Exception:
        logger.exception("Test exception logging")
    
    logger.success("Test task completed")