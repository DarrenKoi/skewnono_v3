import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_storage_data(n_rows=300):
    """
    Generate dummy storage data for CD-SEM equipment.
    
    Args:
        n_rows (int): Number of rows to generate. Default is 300.
        
    Returns:
        pd.DataFrame: DataFrame containing storage data with columns:
            - eqp_id: Equipment ID
            - eqp_ip: Equipment IP address
            - fac_id: Facility ID
            - total: Total storage capacity
            - used: Used storage
            - avail: Available storage
            - percent: Usage percentage
            - storage_mt: Storage metrics timestamp
            - rcp_counts: Recipe counts
            - rcp_counts_mt: Recipe counts timestamp
            - storage_mt_date: Storage metrics date
            - fab_name: Fab name
            - eqp_model_cd: Equipment model code
    """
    # Define possible values based on SEM Lists
    fac_ids = ['M10', 'M11', 'M14', 'M15', 'M16', 'R3']
    fab_suffixes = ['A', 'B', 'C']

    # Equipment model codes by vendor
    hitachi_models = ['CG6300', 'CG6320', 'CG6340', 'CG6360', 'CG6380']
    amat_models = ['TP3000', 'TP3500', 'TP4000', 'TP4500', 'PROVISION_10', 'PROVISION_20', 'VERITYSEM_4', 'VERITYSEM_5']

    # Equipment IDs and prefixes
    eqp_prefixes = {
        'HITACHI': ['ECXDX', 'ECDX', 'HCDX'],
        'AMAT': ['PCD', 'MCD', 'ACD', 'VCD']
    }

    # IP address ranges
    ip_prefixes = ['177', '197']

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

        # Select vendor and model
        vendor = random.choice(['HITACHI', 'AMAT'])
        if vendor == 'HITACHI':
            model = random.choice(hitachi_models)
            eqp_prefix = random.choice(eqp_prefixes['HITACHI'])
        else:
            model = random.choice(amat_models)
            eqp_prefix = random.choice(eqp_prefixes['AMAT'])

        # Generate equipment ID
        eqp_id = f"{eqp_prefix}{random.randint(100, 999)}"

        # Generate IP address
        ip_prefix = random.choice(ip_prefixes)
        eqp_ip = f"{ip_prefix}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

        # Generate storage data
        # Total storage: 500G to 2T
        if random.random() < 0.7:  # 70% chance for GB
            total_gb = random.randint(500, 999)
            total = f"{total_gb}G"
            total_value = total_gb
        else:  # 30% chance for TB
            total_tb = round(random.uniform(1.0, 2.0), 1)
            total = f"{total_tb}T"
            total_value = total_tb * 1024  # Convert to GB for calculations

        # Used storage: 20% to 90% of total
        used_percentage = random.uniform(0.2, 0.9)
        used_value = total_value * used_percentage

        # Format used storage
        if used_value < 1024:
            used = f"{int(used_value)}G"
        else:
            used = f"{round(used_value / 1024, 1)}T"

        # Available storage
        avail_value = total_value - used_value
        if avail_value < 1024:
            avail = f"{int(avail_value)}G"
        else:
            avail = f"{round(avail_value / 1024, 1)}T"

        # Percentage
        percent = f"{int(used_percentage * 100)}%"

        # Generate timestamps for storage metrics
        # storage_mt: within last 7 days
        days_ago = random.uniform(0, 7)
        storage_mt = datetime.now() - timedelta(days=days_ago,
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59),
                                                seconds=random.randint(0, 59),
                                                microseconds=random.randint(0, 999999))

        # storage_mt_date: just the date part
        storage_mt_date = storage_mt.date()

        # Recipe counts: 50 to 500
        rcp_counts = random.randint(50, 500)

        # rcp_counts_mt: usually close to storage_mt but can be different
        rcp_time_diff = random.uniform(-0.5, 0.5)  # +/- 12 hours
        rcp_counts_mt = storage_mt + timedelta(hours=rcp_time_diff,
                                               microseconds=random.randint(0, 999999))

        # Add row to data
        data.append({
            'eqp_id': eqp_id,
            'eqp_ip': eqp_ip,
            'fac_id': fac_id,
            'total': total,
            'used': used,
            'avail': avail,
            'percent': percent,
            'storage_mt': storage_mt,
            'rcp_counts': rcp_counts,
            'rcp_counts_mt': rcp_counts_mt,
            'storage_mt_date': storage_mt_date,
            'fab_name': fab_name,
            'eqp_model_cd': model
        })

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Set appropriate data types
    df['eqp_id'] = df['eqp_id'].astype('string')
    df['eqp_ip'] = df['eqp_ip'].astype('string')
    df['fac_id'] = df['fac_id'].astype('string')
    df['total'] = df['total'].astype('string')
    df['used'] = df['used'].astype('string')
    df['avail'] = df['avail'].astype('string')
    df['percent'] = df['percent'].astype('string')
    df['storage_mt'] = pd.to_datetime(df['storage_mt'])
    df['rcp_counts'] = df['rcp_counts'].astype('int64')
    df['rcp_counts_mt'] = pd.to_datetime(df['rcp_counts_mt'])
    df['storage_mt_date'] = pd.to_datetime(df['storage_mt_date'])
    df['fab_name'] = df['fab_name'].astype('string')
    df['eqp_model_cd'] = df['eqp_model_cd'].astype('string')
    
    return df

# Create a default dataframe instance that can be imported
df = generate_storage_data()