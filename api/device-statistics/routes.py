from flask import Blueprint, jsonify, request
import platform
import os

# Create the blueprint
device_statistics_bp = Blueprint('device_statistics', __name__)

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
    from .real import device_info
else:
    from .dummy import device_info

@device_statistics_bp.route('/device-options', methods=['GET'])
def get_device_options():
    """
    Get device options based on fac_id parameter.
    If fac_id is 'R3', return DRAM, NAND, NM options.
    Otherwise, return list of device names.
    """
    fac_id = request.args.get('fac_id', '')
    
    if fac_id == 'R3':
        # Return R3 specific options
        options = device_info.get_r3_options()
    else:
        # Return general device names
        options = device_info.get_device_names()
    
    return jsonify({
        'fac_id': fac_id,
        'options': options
    })

@device_statistics_bp.route('/device-data', methods=['GET'])
def get_device_data():
    """
    Get device statistics data based on fac_id and selected option.
    """
    fac_id = request.args.get('fac_id', '')
    selected_option = request.args.get('option', '')
    
    if fac_id == 'R3':
        # Get R3 specific data based on selected option (DRAM, NAND, NM)
        data = device_info.get_r3_data(selected_option)
    else:
        # Get device specific data based on selected device name
        data = device_info.get_device_data(selected_option)
    
    return jsonify({
        'fac_id': fac_id,
        'selected_option': selected_option,
        'data': data
    })

@device_statistics_bp.route('/all-data', methods=['GET'])
def get_all_data():
    """
    Get all device statistics data (legacy endpoint).
    """
    data = device_info.get_all_data()
    return jsonify(data)