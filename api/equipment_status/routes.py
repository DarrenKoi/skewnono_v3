from flask import Blueprint, jsonify
import os
from utils.auth import require_access

# Create blueprint
equipment_status_bp = Blueprint('equipment_status', __name__, url_prefix='/equipment-status')

# Environment detection - determine which data source to use
def get_data_source():
    """Determine data source based on DATA_SOURCE_MODE environment variable"""
    env_mode = os.environ.get('DATA_SOURCE_MODE')
    if env_mode in ['dummy', 'real']:
        return env_mode
    
    # Default to dummy if no environment variable is set
    return 'dummy'

# Import appropriate data modules based on environment
data_source = get_data_source()
if data_source == 'real':
    from .real import sem_lists, storage
    # TODO: Add not_available module for real environment
else:
    from .dummy import sem_lists, storage, not_available


@equipment_status_bp.route('/current-status', methods=['GET'])
@require_access
def get_equipment_status():
    """Get current equipment status using environment-aware data loading"""
    try:
        # Use the imported data module based on environment
        df = sem_lists.df
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


@equipment_status_bp.route('/storage', methods=['GET'])
@require_access
def get_equipment_storage():
    """Get equipment storage information using environment-aware data loading"""
    try:
        # Use the imported data module based on environment
        df = storage.df
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


@equipment_status_bp.route('/not_available', methods=['GET'])
@require_access
def get_not_available_equipment():
    """Get equipment that is not available (Off status, empty version, or empty storage)"""
    try:
        # Only available in dummy environment for now
        if data_source != 'dummy':
            return jsonify({
                'status': 'error',
                'message': 'Not available endpoint only supported in development environment'
            }), 501
        
        # Get data from the three not_available functions
        off_equipment = not_available.not_available_for_now()
        empty_version_equipment = not_available.version_not_available()
        empty_storage_equipment = not_available.storage_not_available()
        
        return jsonify({
            'status': 'success',
            'data': {
                'equipment_off': off_equipment,
                'version_empty': empty_version_equipment,
                'storage_empty': empty_storage_equipment
            },
            'counts': {
                'equipment_off': len(off_equipment),
                'version_empty': len(empty_version_equipment),
                'storage_empty': len(empty_storage_equipment)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500