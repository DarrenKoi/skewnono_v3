from flask import Blueprint, jsonify, request
import platform
import os

# Create blueprint
recipe_search_bp = Blueprint('recipe_search', __name__)

# Environment detection
def get_data_source():
    env_override = os.environ.get('DATA_SOURCE_MODE')
    if env_override in ['dummy', 'real']:
        return env_override
    
    node_name = platform.node().upper()
    if node_name.startswith('DESKTOP'):
        return 'dummy'  # Home environment
    elif node_name.startswith('PC') or 'SKEWNONO' in node_name:
        return 'real'   # Work/production environment
    else:
        return 'dummy'  # Default

# Import appropriate data modules based on environment
data_source = get_data_source()
if data_source == 'real':
    # Import real data modules when implemented
    pass
else:
    from .dummy import meas_hist
    from .dummy import recipe_open_data

@recipe_search_bp.route('/<fac_id>/<tool_category>/recipe-open/<recipe_id>', methods=['GET'])
def get_recipe_open_data(fac_id, tool_category, recipe_id):
    """Get recipe open data including wafer_mp_info, wafer_align_info, and idp_image_info"""
    try:
        if data_source == 'dummy':
            # Get dummy data with fac_id and tool_category
            data = recipe_open_data.get_recipe_open_data(recipe_id, fac_id, tool_category)
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            # Real data implementation would go here
            return jsonify({
                'success': False,
                'error': 'Real data source not implemented'
            }), 501
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_search_bp.route('/meas-hist', methods=['GET'])
def get_meas_hist():
    """Get measurement history data"""
    try:
        if data_source == 'dummy':
            # Get dummy data
            df = meas_hist.df
            return jsonify({
                'success': True,
                'data': df.to_dict('records')
            })
        else:
            # Real data implementation would go here
            return jsonify({
                'success': False,
                'error': 'Real data source not implemented'
            }), 501
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500