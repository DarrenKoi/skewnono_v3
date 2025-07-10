import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define the number of rows
n_rows = 300

# Define possible values based on SEM Lists
fac_ids = ['M10', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'R3', 'R4', 'R5']
fab_suffixes = ['A', 'B', 'C', 'D']

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
                                            seconds=random.randint(0, 59))

    # storage_mt_date: just the date part
    storage_mt_date = storage_mt.date()

    # Recipe counts: 50 to 500
    rcp_counts = random.randint(50, 500)

    # rcp_counts_mt: usually close to storage_mt but can be different
    rcp_time_diff = random.uniform(-0.5, 0.5)  # +/- 12 hours
    rcp_counts_mt = storage_mt + timedelta(hours=rcp_time_diff)

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

# Display first 10 rows and basic info
print("First 10 rows of the generated storage data:")
print(df.head(10))
print("\nDataFrame Info:")
print(df.info())
print("\nDataFrame Shape:", df.shape)

# Display some statistics
print("\nStorage Statistics:")
print("Facility distribution:")
print(df['fac_id'].value_counts().head())
print("\nModel distribution:")
print(df['eqp_model_cd'].value_counts().head())

# Show storage utilization distribution
percent_values = df['percent'].str.rstrip('%').astype(int)
print("\nStorage Utilization Statistics:")
print(f"Mean utilization: {percent_values.mean():.1f}%")
print(f"Min utilization: {percent_values.min()}%")
print(f"Max utilization: {percent_values.max()}%")

# Recipe count statistics
print("\nRecipe Count Statistics:")
print(f"Mean recipe count: {df['rcp_counts'].mean():.1f}")
print(f"Min recipe count: {df['rcp_counts'].min()}")
print(f"Max recipe count: {df['rcp_counts'].max()}")

# Create sample_data folder if it doesn't exist
import os

folder_path = 'sample_data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"\nCreated folder: {folder_path}")

# Save to CSV
csv_filename = os.path.join(folder_path, 'cd_sem_storage_dummy_data.csv')
df.to_csv(csv_filename, index=False)
print(f"\nData exported to: {csv_filename}")

# Optional: Save to JSON for web applications
json_filename = os.path.join(folder_path, 'cd_sem_storage_dummy_data.json')
df.to_json(json_filename, orient='records', date_format='iso')
print(f"JSON data exported to: {json_filename}")

# Create a sample for web development (first 20 rows)
sample_df = df.head(20)
sample_json = sample_df.to_json(orient='records', date_format='iso')
with open(os.path.join(folder_path, 'cd_sem_storage_sample.json'), 'w') as f:
    f.write(sample_json)
print("Sample JSON (20 rows) exported for web development")