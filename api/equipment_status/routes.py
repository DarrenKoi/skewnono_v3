from flask import jsonify
from . import equipment_status_bp


@equipment_status_bp.route('/current-status', methods=['GET'])
def get_equipment_status():
    """Get current equipment status from sem_lists.py"""
    try:
        # Import the dataframe from sem_lists.py
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from api.dummy.sem_lists import df
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


@equipment_status_bp.route('/storage', methods=['GET'])
def get_equipment_storage():
    """Get equipment storage information from storage.py"""
    try:
        # Import the dataframe from storage.py
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from api.dummy.storage import df
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