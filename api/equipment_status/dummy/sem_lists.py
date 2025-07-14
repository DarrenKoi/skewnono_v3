import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_equipment_data(n_rows=300):
    """
    Generate dummy equipment data for SEM (Scanning Electron Microscope) equipment.
    
    Args:
        n_rows (int): Number of rows to generate. Default is 300.
        
    Returns:
        pd.DataFrame: DataFrame containing equipment data with columns:
            - fac_id: Facility ID
            - eqp_id: Equipment ID
            - eqp_model_cd: Equipment model code
            - eqp_grp_id: Equipment group ID
            - vendor_nm: Vendor name
            - eqp_ip: Equipment IP address
            - fab_name: Fab name
            - updt_dt: Update datetime
            - available: Availability status (On/Off)
            - version: Version number
    """
    # Define possible values for each column
    fac_ids = ['M10', 'M11', 'M14', 'M15', 'M16', 'R3']
    fab_suffixes = ['A', 'B', 'C']
    
    # Equipment model codes by vendor
    hitachi_models = ['CG6300', 'CG6320', 'CG6340', 'CG6360', 'CG6380']
    amat_models = ['TP3000', 'TP3500', 'TP4000', 'TP4500', 'PROVISION_10', 'PROVISION_20', 'VERITYSEM_4', 'VERITYSEM_5']
    
    # Equipment group prefixes
    eqp_grp_prefixes = ['G-ECD-', 'G-MCD-', 'G-KCD-', 'G-MDS-', 'G-PCD-', 'G-ACD-']
    
    # Generate data
    data = []
    
    for i in range(n_rows):
        # Select facility and fab
        fac_id = random.choice(fac_ids)
        # Special case: R3 can have R4 fab name
        if fac_id == 'R3' and random.random() < 0.3:
            fab_name = 'R4'
        else:
            fab_name = fac_id + random.choice(fab_suffixes)
        
        # Select vendor
        vendor = random.choice(['HITACHI', 'AMAT'])
        
        # Select model based on vendor
        if vendor == 'HITACHI':
            model = random.choice(hitachi_models)
            eqp_prefix = random.choice(['ECXDX', 'ECDX', 'HCDX'])
        else:
            model = random.choice(amat_models)
            eqp_prefix = random.choice(['PCD', 'MCD', 'ACD', 'VCD'])
        
        # Generate equipment ID
        eqp_id = f"{eqp_prefix}{random.randint(100, 999)}"
        
        # Generate equipment group ID
        eqp_grp_id = f"{random.choice(eqp_grp_prefixes)}{random.randint(1, 3):02d}"
        
        # Generate IP address (using 177.x.x.x or 197.x.x.x ranges)
        ip_prefix = random.choice(['177', '197'])
        eqp_ip = f"{ip_prefix}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        
        # Generate update date (within last 90 days)
        days_ago = random.randint(0, 90)
        updt_dt = datetime.now() - timedelta(days=days_ago)
        
        # Equipment availability (90% chance of being "On")
        available = "On" if random.random() < 0.9 else "Off"
        
        # Version (1-3)
        version = random.randint(1, 3)
        
        # Add row to data
        data.append({
            'fac_id': fac_id,
            'eqp_id': eqp_id,
            'eqp_model_cd': model,
            'eqp_grp_id': eqp_grp_id,
            'vendor_nm': vendor,
            'eqp_ip': eqp_ip,
            'fab_name': fab_name,
            'updt_dt': updt_dt,
            'available': available,
            'version': version
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Set appropriate data types
    df['fac_id'] = df['fac_id'].astype('string')
    df['eqp_id'] = df['eqp_id'].astype('string')
    df['eqp_model_cd'] = df['eqp_model_cd'].astype('string')
    df['eqp_grp_id'] = df['eqp_grp_id'].astype('string')
    df['vendor_nm'] = df['vendor_nm'].astype('string')
    df['eqp_ip'] = df['eqp_ip'].astype('string')
    df['fab_name'] = df['fab_name'].astype('string')
    df['updt_dt'] = pd.to_datetime(df['updt_dt'])
    df['available'] = df['available'].astype('string')
    df['version'] = df['version'].astype('int64')
    
    return df

# Create a default dataframe instance that can be imported
df = generate_equipment_data()