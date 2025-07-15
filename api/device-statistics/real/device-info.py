def get_r3_options():
    """
    Returns the three R3 facility options.
    
    Returns:
        list: List of R3 options ["DRAM", "NAND", "NM"]
    """
    return ["DRAM", "NAND", "NM"]


def get_device_names():
    """
    Returns a list of device names for non-R3 facilities.
    In real implementation, this would fetch from database/API.
    
    Returns:
        list: List of device names
    """
    # TODO: Replace with actual database/API call
    # This is a placeholder for the real implementation
    return [
        "REAL-DEV-001",
        "REAL-DEV-002", 
        "REAL-DEV-003",
        "REAL-DEV-004",
        "REAL-DEV-005",
        "REAL-DEV-006",
        "REAL-DEV-007",
        "REAL-DEV-008",
        "REAL-DEV-009",
        "REAL-DEV-010"
    ]


def get_r3_data(option):
    """
    Returns device statistics data for R3 facility based on selected option.
    In real implementation, this would fetch from database/API.
    
    Args:
        option (str): Selected R3 option ("DRAM", "NAND", or "NM")
        
    Returns:
        dict: Device statistics data for the selected R3 option
    """
    if option not in ["DRAM", "NAND", "NM"]:
        return {"error": "Invalid R3 option"}
    
    # TODO: Replace with actual database/API call
    # This is a placeholder for the real implementation
    return {
        "option": option,
        "facility": "R3",
        "data": [],  # Would be populated from real data source
        "summary": {}  # Would be populated from real data source
    }


def get_device_data(device_name):
    """
    Returns device statistics data for a specific device name.
    In real implementation, this would fetch from database/API.
    
    Args:
        device_name (str): Selected device name
        
    Returns:
        dict: Device statistics data for the selected device
    """
    if not device_name:
        return {"error": "Device name is required"}
    
    # TODO: Replace with actual database/API call
    # This is a placeholder for the real implementation
    return {
        "device_name": device_name,
        "facility": "Non-R3",
        "data": [],  # Would be populated from real data source
        "summary": {}  # Would be populated from real data source
    }


def get_all_data():
    """
    Returns all device statistics data (legacy function).
    In real implementation, this would fetch from database/API.
    
    Returns:
        dict: All device statistics data
    """
    # TODO: Replace with actual database/API call
    # This is a placeholder for the real implementation
    return {
        "all_rcp_info": [],
        "only_normal_rcp_info": [],
        "mother_normal_rcp_info": [],
        "only_sample_rcp_info": []
    }