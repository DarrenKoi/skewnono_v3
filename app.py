import logging
import atexit
import os
from flask import Flask
from config import Config
from api.routes import api_bp
from scheduled_tasks.scheduler import create_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return {'message': 'Flask server with scheduler is running'}

    return app


def setup_scheduler(app):
    """Setup and start scheduler"""
    # Only start scheduler if we're in the main worker
    worker_id = os.environ.get('UWSGI_WORKER_ID', '')

    if worker_id == '' or worker_id == '0':
        scheduler = create_scheduler()
        scheduler.start()

        # Shutdown scheduler when app stops
        atexit.register(lambda: scheduler.shutdown(wait=False))

        # Add scheduler to app context
        app.scheduler = scheduler

        logger.info(f"Scheduler started successfully in worker {worker_id or 'main'}")
    else:
        logger.info(f"Skipping scheduler in worker {worker_id}")
        app.scheduler = None

    return app.scheduler


# Create application instance for uWSGI
application = create_app()
setup_scheduler(application)

if __name__ == '__main__':
    # Development mode (not uWSGI)
    setup_scheduler(application)
    application.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)