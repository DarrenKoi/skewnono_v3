from flask import Blueprint, jsonify, request
from datetime import datetime
from .utils.redis_client import redis_client

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check Redis connectivity
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'redis': redis_status
    })


@api_bp.route('/fab-list', methods=['GET'])
def get_fab_list():
    fab_list_dict = {
        "R3": ["R3", "R4"],
        "M16": ["M16A", "M16B", "M16E"],
        "M15": ["M15A", "M15B"],
        "M14": ["M14A", "M14B"],
        "M11": ["M11A", "M11B"],
        "M10": ["M10A", "M10B"]
    }

    """Get fab list dictionary"""
    return jsonify(fab_list_dict)


@api_bp.route('/jobs/status', methods=['GET'])
def get_jobs_status():
    """Get status of all scheduled jobs"""
    from flask import current_app

    if hasattr(current_app, 'scheduler'):
        jobs = []
        for job in current_app.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        return jsonify({'jobs': jobs})
    else:
        return jsonify({'error': 'Scheduler not available'}), 503


@api_bp.route('/users', methods=['GET'])
def get_users():
    """Example API endpoint"""
    # Your API logic here
    return jsonify({
        'users': [
            {'id': 1, 'name': 'User 1'},
            {'id': 2, 'name': 'User 2'}
        ]
    })


@api_bp.route('/users', methods=['POST'])
def create_user():
    """Example POST endpoint"""
    data = request.get_json()
    # Your API logic here
    return jsonify({
        'message': 'User created',
        'data': data
    }), 201


# Add more API endpoints as needed