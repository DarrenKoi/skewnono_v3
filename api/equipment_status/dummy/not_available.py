import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from . import sem_lists, storage

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def not_available_for_now():
    """
    Returns equipment data where available status is "Off".
    
    Returns:
        list: List of dictionaries containing equipment data with available="Off"
    """
    df = sem_lists.df
    off_equipment = df[df['available'] == 'Off']
    return off_equipment.to_dict('records')

def version_not_available():
    """
    Returns equipment data where version is empty or empty string.
    Since sem_lists.py generates integer versions (1-3), this function
    modifies some random entries to have empty/null versions.
    
    Returns:
        list: List of dictionaries containing equipment data with empty versions
    """
    df = sem_lists.df.copy()
    
    # Randomly set 10% of equipment to have empty versions
    sample_size = max(1, int(len(df) * 0.1))
    random_indices = np.random.choice(df.index, size=sample_size, replace=False)
    
    # To avoid FutureWarning, cast to a type that can hold both numbers and strings (object).
    df['version'] = df['version'].astype(object)

    # Set version to empty string for selected equipment
    df.loc[random_indices, 'version'] = ""
    
    # Filter for equipment with empty versions
    empty_version_equipment = df[df['version'] == ""]
    return empty_version_equipment.to_dict('records')

def storage_not_available():
    """
    Returns storage data where storage fields are empty or empty string.
    This function modifies some random entries to have empty storage values.
    
    Returns:
        list: List of dictionaries containing storage data with empty storage fields
    """
    df = storage.df.copy()
    
    # Randomly set 15% of storage entries to have empty storage fields
    sample_size = max(1, int(len(df) * 0.15))
    random_indices = np.random.choice(df.index, size=sample_size, replace=False)
    
    # Set storage fields to empty string for selected equipment
    storage_fields = ['total', 'used', 'avail', 'percent']
    for field in storage_fields:
        df.loc[random_indices, field] = ""
    
    # Filter for storage entries with empty storage fields
    empty_storage = df[df['total'] == ""]
    return empty_storage.to_dict('records')

# Generate data instances for easy access
not_available_data = not_available_for_now()
version_not_available_data = version_not_available()
storage_not_available_data = storage_not_available()