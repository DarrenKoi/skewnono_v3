from flask import Blueprint, jsonify, request
import os
import pandas as pd
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

@device_statistics_bp.route('/device-data', methods=['GET'])
@require_access
def get_device_data():
    """
    Get all R3 device statistics data.
    
    Returns data with dates as top-level keys, each containing:
    - all_rcp_info, only_normal_rcp_info, mother_normal_rcp_info, only_sample_rcp_info
    - all_summary, only_normal_summary, mother_normal_summary, only_sample_summary  
    - all_recipe_list
    
    Plus special keys:
    - working_devices: prod_id to prod_catg_cd2 mapping
    - device_options: device categories (DRAM, NAND, NM) with their prod_ids
    """
    # Get all data (no filtering)
    raw_result = device_info.get_all_data()
    
    if 'error' in raw_result:
        return jsonify(raw_result)
    
    # Restructure the data to have dates as top-level keys
    restructured_data = {}
    
    # Add working_devices mapping
    restructured_data['working_devices'] = device_info.get_working_devices_mapping()
    
    # Add device options for reference
    restructured_data['device_options'] = device_info.get_r3_options()
    
    # Process weekly data
    if 'weekly_data' in raw_result:
        for date_key, week_data in raw_result['weekly_data'].items():
            # Flatten the structure for each date
            date_data = {}
            
            # Extract recipe info data
            if 'rcp_info' in week_data:
                date_data['all_rcp_info'] = week_data['rcp_info'].get('all_rcp_info', [])
                date_data['only_normal_rcp_info'] = week_data['rcp_info'].get('only_normal_rcp_info', [])
                date_data['mother_normal_rcp_info'] = week_data['rcp_info'].get('mother_normal_rcp_info', [])
                date_data['only_sample_rcp_info'] = week_data['rcp_info'].get('only_sample_rcp_info', [])
            
            # Extract summary data by category
            if 'summary_by_category' in week_data:
                date_data['all_summary'] = week_data['summary_by_category'].get('all_summary', [])
                date_data['only_normal_summary'] = week_data['summary_by_category'].get('only_normal_summary', [])
                date_data['mother_normal_summary'] = week_data['summary_by_category'].get('mother_normal_summary', [])
                date_data['only_sample_summary'] = week_data['summary_by_category'].get('only_sample_summary', [])
            
            # Add all_recipe_list
            recipe_list_data = week_data.get('all_recipe_list', [])
            if recipe_list_data:
                # Data is already in the correct format (list of dicts with proper columns)
                date_data['all_recipe_list'] = recipe_list_data
            else:
                date_data['all_recipe_list'] = []
            
            # Add this date's data to the restructured result
            restructured_data[date_key] = date_data
    
    print(f"[DEBUG] Restructured data keys: {list(restructured_data.keys())[:5]}...")  # Show first 5 keys
    print(f"[DEBUG] Total dates: {len([k for k in restructured_data.keys() if k not in ['working_devices', 'device_options']])}")
    
    return jsonify(restructured_data)

