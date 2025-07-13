import logging
import atexit
import os
from flask import Flask, request, redirect
from flask_cors import CORS
from config import Config
from api.routes import api_bp


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# TODO: Move scheduler creation and configuration to a dedicated module.
def create_scheduler():
    """
    Creates and returns a scheduler instance.
    This is a placeholder. The actual implementation should initialize
    and configure APScheduler or another scheduling library.
    """
    class MockScheduler:
        def start(self):
            logger.info("Mock scheduler started.")
        def shutdown(self, wait=True):
            logger.info("Mock scheduler shutdown.")
    return MockScheduler()


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
    Simplified scheduler setup.
    Initializes and starts the scheduler.
    """
    # TODO: In a production environment with multiple workers (e.g., uWSGI),
    # ensure this only runs in a single process to avoid duplicate jobs.
    try:
        scheduler = create_scheduler()
        scheduler.start()

        # Shutdown scheduler when app stops
        atexit.register(lambda: scheduler.shutdown(wait=False))

        app.scheduler = scheduler
        logger.info("Scheduler initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")
        app.scheduler = None

    return app.scheduler


# Create application instance for uWSGI
application = create_app()
setup_scheduler(application)

if __name__ == '__main__':
    # Development mode (not uWSGI)
    setup_scheduler(application)
    application.run(host='0.0.0.0', port=5000, debug=True)