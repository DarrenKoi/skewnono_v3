"""
APScheduler configuration with proper logging support.
This module handles all scheduled background tasks with centralized logging.
"""
import os
import atexit
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from .app_logger import get_app_logger, get_task_logger

# Get the main application logger
logger = get_app_logger()

class SchedulerManager:
    """Manages the APScheduler instance with proper logging"""
    
    def __init__(self):
        self.scheduler = None
        self._initialized = False
        
    def init_scheduler(self):
        """Initialize the scheduler with proper configuration"""
        if self._initialized:
            logger.warning("Scheduler already initialized, skipping...")
            return self.scheduler
            
        try:
            # Create scheduler instance
            self.scheduler = BackgroundScheduler(
                daemon=True,
                timezone='UTC',
                job_defaults={
                    'coalesce': True,
                    'max_instances': 1,
                    'misfire_grace_time': 30
                }
            )
            
            # Add event listeners for job monitoring
            self.scheduler.add_listener(
                self._job_executed_listener,
                EVENT_JOB_EXECUTED
            )
            self.scheduler.add_listener(
                self._job_error_listener,
                EVENT_JOB_ERROR
            )
            self.scheduler.add_listener(
                self._job_missed_listener,
                EVENT_JOB_MISSED
            )
            
            # Start the scheduler
            self.scheduler.start()
            self._initialized = True
            
            # Register cleanup on exit
            atexit.register(self.shutdown)
            
            logger.success("Scheduler initialized successfully", 
                         jobs_count=len(self.scheduler.get_jobs()))
            
            return self.scheduler
            
        except Exception as e:
            logger.exception("Failed to initialize scheduler")
            raise
    
    def _job_executed_listener(self, event):
        """Log successful job execution"""
        job = self.scheduler.get_job(event.job_id)
        if job:
            logger.info("Scheduled job executed successfully",
                       job_id=event.job_id,
                       job_name=job.name,
                       scheduled_time=event.scheduled_run_time,
                       execution_time=datetime.now())
    
    def _job_error_listener(self, event):
        """Log job execution errors"""
        job = self.scheduler.get_job(event.job_id)
        if job:
            logger.error("Scheduled job failed with error",
                        job_id=event.job_id,
                        job_name=job.name,
                        exception=str(event.exception),
                        traceback=event.traceback)
    
    def _job_missed_listener(self, event):
        """Log missed job executions"""
        job = self.scheduler.get_job(event.job_id)
        if job:
            logger.warning("Scheduled job execution missed",
                          job_id=event.job_id,
                          job_name=job.name,
                          scheduled_time=event.scheduled_run_time)
    
    def add_job(self, func, trigger, **kwargs):
        """
        Add a job to the scheduler with automatic logging wrapper
        
        Args:
            func: The function to schedule
            trigger: The trigger type ('interval', 'cron', 'date')
            **kwargs: Additional arguments for add_job
        """
        # Get job name from function or kwargs
        job_name = kwargs.get('name', func.__name__)
        
        # Create a wrapper that adds logging context
        def logged_job_wrapper():
            task_logger = get_task_logger(job_name)
            task_logger.info(f"Starting scheduled task: {job_name}")
            
            try:
                result = func()
                task_logger.success(f"Completed scheduled task: {job_name}")
                return result
            except Exception as e:
                task_logger.exception(f"Error in scheduled task: {job_name}")
                raise
        
        # Add the wrapped job
        kwargs['name'] = job_name
        job = self.scheduler.add_job(logged_job_wrapper, trigger, **kwargs)
        
        logger.info(f"Added scheduled job: {job_name}",
                   trigger=trigger,
                   job_id=job.id,
                   next_run=job.next_run_time)
        
        return job
    
    def get_jobs_status(self):
        """Get status of all scheduled jobs"""
        if not self.scheduler:
            return {"status": "not_initialized", "jobs": []}
        
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "pending": job.pending
            })
        
        return {
            "status": "running" if self.scheduler.running else "stopped",
            "jobs_count": len(jobs),
            "jobs": jobs
        }
    
    def shutdown(self, wait=True):
        """Shutdown the scheduler gracefully"""
        if self.scheduler and self.scheduler.running:
            logger.info("Shutting down scheduler...")
            self.scheduler.shutdown(wait=wait)
            self._initialized = False
            logger.success("Scheduler shutdown complete")

# Global scheduler instance
scheduler_manager = SchedulerManager()

def get_scheduler():
    """Get the global scheduler instance"""
    if not scheduler_manager._initialized:
        scheduler_manager.init_scheduler()
    return scheduler_manager.scheduler

def add_scheduled_job(func, trigger, **kwargs):
    """Convenience function to add a job to the global scheduler"""
    return scheduler_manager.add_job(func, trigger, **kwargs)