import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define the number of rows
n_rows = 300

# Define possible values for each column
fac_ids = ['M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'R3', 'R4', 'R5']
fab_suffixes = ['A', 'B', 'C', 'D']

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
    ip_address = f"{ip_prefix}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

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
        'ip_address': ip_address,  # Fixed column name from 'eqp_id' to 'ip_address'
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
df['ip_address'] = df['ip_address'].astype('string')
df['fab_name'] = df['fab_name'].astype('string')
df['updt_dt'] = pd.to_datetime(df['updt_dt'])
df['available'] = df['available'].astype('string')
df['version'] = df['version'].astype('int64')

# Display first 10 rows and basic info
print("First 10 rows of the generated data:")
print(df.head(10))
print("\nDataFrame Info:")
print(df.info())
print("\nDataFrame Shape:", df.shape)
print("\nValue counts for categorical columns:")
print("\nVendor distribution:")
print(df['vendor_nm'].value_counts())
print("\nAvailability status:")
print(df['available'].value_counts())
print("\nVersion distribution:")
print(df['version'].value_counts())

# Create sample_data folder if it doesn't exist
import os

folder_path = 'sample_data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"\nCreated folder: {folder_path}")

# Save to CSV in sample_data folder
csv_filename = os.path.join(folder_path, 'cd_sem_dummy_data.csv')
df.to_csv(csv_filename, index=False)
print(f"\nData exported to: {csv_filename}")

# If you want to use this data in your web application, you can convert it to JSON
# json_data = df.to_json(orient='records', date_format='iso')
# with open(os.path.join(folder_path, 'cd_sem_dummy_data.json'), 'w') as f:
#     f.write(json_data)
# print("JSON data also exported to sample_data folder")