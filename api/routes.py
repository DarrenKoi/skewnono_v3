from flask import Blueprint, jsonify, request
from datetime import datetime
from utils.redis_client import redis_client

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

@api_bp.route('/equipment-status/current-status', methods=['GET'])
def get_equipment_status():
    """Get current equipment status from sem_lists.py"""
    try:
        # Import the dataframe from sem_lists.py
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from dummy.sem_lists import df
        print(df.head(5))
        # Convert dataframe to dictionary format for JSON response
        equipment_data = df.to_dict('records')
        
        # Convert datetime to ISO format string for JSON serialization
        for record in equipment_data:
            if 'updt_dt' in record and hasattr(record['updt_dt'], 'isoformat'):
                record['updt_dt'] = record['updt_dt'].isoformat()

        return jsonify({
            'status': 'success',
            'data': equipment_data,
            'total': len(equipment_data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@api_bp.route('/equipment-status/storage', methods=['GET'])
def get_equipment_storage():
    """Get equipment storage information from storage.py"""
    try:
        # Import the dataframe from storage.py
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from dummy.storage import df
        print(df.head(5))
        # Convert dataframe to dictionary format for JSON response
        storage_data = df.to_dict('records')
        
        # Convert datetime fields to ISO format string for JSON serialization
        for record in storage_data:
            # Convert storage_mt
            if 'storage_mt' in record and hasattr(record['storage_mt'], 'isoformat'):
                record['storage_mt'] = record['storage_mt'].isoformat()
            
            # Convert rcp_counts_mt
            if 'rcp_counts_mt' in record and hasattr(record['rcp_counts_mt'], 'isoformat'):
                record['rcp_counts_mt'] = record['rcp_counts_mt'].isoformat()
            
            # Convert storage_mt_date
            if 'storage_mt_date' in record and hasattr(record['storage_mt_date'], 'isoformat'):
                record['storage_mt_date'] = record['storage_mt_date'].isoformat()

        return jsonify({
            'status': 'success',
            'data': storage_data,
            'total': len(storage_data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# Add more API endpoints as needed