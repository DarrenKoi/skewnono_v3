import os
import atexit
from flask import Flask, request, redirect
from flask_cors import CORS
from config import Config
from api.routes import api_bp
from api.equipment_status.routes import equipment_status_bp
from api.device_statistics.routes import device_statistics_bp
from api.recipe_search.routes import recipe_search_bp
from api.utils.app_logger import logger, cleanup_logger
from api.utils.scheduler import scheduler_manager, get_scheduler
from api.scheduled_tasks import register_scheduled_tasks


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(equipment_status_bp, url_prefix='/api/equipment-status')
    app.register_blueprint(device_statistics_bp, url_prefix='/api/device-statistics')
    app.register_blueprint(recipe_search_bp, url_prefix='/api/recipe-search')

    @app.before_request
    def force_http():
        """Redirect HTTPS requests to HTTP"""
        if request.is_secure:
            return redirect(request.url.replace('https://', 'http://'), code=301)

    @app.route('/')
    def index():
        return {'message': 'Flask server with scheduler is running'}

    return app


def setup_scheduler(app):
    """
    Initialize and configure the APScheduler.
    """
    # In production with uWSGI, check if we're in the main worker
    # to avoid duplicate scheduled tasks
    try:
        import uwsgi
        # Only initialize scheduler in the first worker
        if uwsgi.worker_id() != 1:
            logger.info(f"Skipping scheduler initialization in worker {uwsgi.worker_id()}")
            return None
    except ImportError:
        # Not running under uWSGI (development mode)
        pass
    
    try:
        # Initialize the scheduler
        scheduler = scheduler_manager.init_scheduler()
        
        # Register all scheduled tasks
        register_scheduled_tasks()
        
        # Store scheduler reference in app
        app.scheduler = scheduler
        
        logger.success("Scheduler setup completed",
                     jobs_count=len(scheduler.get_jobs()))
        
        return scheduler
    except Exception as e:
        logger.exception("Failed to setup scheduler")
        app.scheduler = None
        return None


# Create application instance for uWSGI
application = create_app()
setup_scheduler(application)

if __name__ == '__main__':
    # Development mode (not uWSGI)
    setup_scheduler(application)
    # Register cleanup on exit
    atexit.register(cleanup_logger)
    application.run(host='0.0.0.0', port=5000, debug=True)