from flask import Blueprint, jsonify, request
import os
from utils.auth import require_access

# Create the blueprint
device_statistics_bp = Blueprint('device_statistics', __name__)

# Environment detection
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
    from api.device_statistics.real import device_info
else:
    from api.device_statistics.dummy import device_info

print(f"[DEBUG] Using data source: {data_source}")

@device_statistics_bp.route('/device-options', methods=['GET'])
@require_access
def get_device_options():
    """
    Get device options based on fac_id parameter.
    If fac_id is 'R3', return DRAM, NAND, NM options with their prod_ids.
    Otherwise, return list of device names.
    """
    fac_id = request.args.get('fac_id', '')
    
    if fac_id == 'R3':
        # Return R3 specific options with prod_ids
        result = device_info.get_r3_options()
        print(f"[DEBUG] R3 options: {result}")
        return jsonify(result)
    else:
        # Return general device names
        options = device_info.get_device_names()
        result = {
            'fac_id': fac_id,
            'options': options
        }
        print(f"[DEBUG] Device options for {fac_id}: {result}")
        return jsonify(result)

@device_statistics_bp.route('/device-data', methods=['GET'])
@require_access
def get_device_data():
    """
    Get device statistics data based on fac_id and selected option.
    Returns weekly data structure with rcp_info, summary, and all_recipe_list.
    Supports filtering by specific product IDs.
    """
    fac_id = request.args.get('fac_id', '')
    selected_option = request.args.get('option', '')
    prod_ids = request.args.getlist('prod_ids[]')  # Get array of product IDs
    
    print(f"[DEBUG] Request params - fac_id: {fac_id}, option: {selected_option}, prod_ids: {prod_ids}")
    
    if fac_id == 'R3':
        # Get R3 specific data based on selected option (DRAM, NAND, NM)
        # This returns weekly data with nested structure
        result = device_info.get_r3_data(selected_option, prod_ids)
        print(f"[DEBUG] R3 data keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        if 'weekly_data' in result:
            week_keys = list(result['weekly_data'].keys())[:2]  # First 2 weeks
            print(f"[DEBUG] First 2 week keys: {week_keys}")
            if week_keys:
                first_week = result['weekly_data'][week_keys[0]]
                print(f"[DEBUG] First week data keys: {list(first_week.keys()) if isinstance(first_week, dict) else 'Not a dict'}")
        return jsonify(result)
    else:
        # Get device specific data based on selected device name
        data = device_info.get_device_data(selected_option)
        result = {
            'fac_id': fac_id,
            'selected_option': selected_option,
            'data': data
        }
        print(f"[DEBUG] Non-R3 data: {list(result.keys())}")
        return jsonify(result)

@device_statistics_bp.route('/all-data', methods=['GET'])
@require_access
def get_all_data():
    """
    Get all device statistics data (legacy endpoint).
    """
    data = device_info.get_all_data()
    print(f"[DEBUG] All data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
    return jsonify(data)