import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def generate_meas_hist_dummy_data(n_rows=500):
    """
    Generate dummy data for CD-SEM measurement history table
    Based on project knowledge and semiconductor manufacturing patterns
    """

    # Equipment data from actual facility mapping
    facility_mapping = {
        "M10": ["M10C", "M10A"],
        "M11": ["M11A", "M11B"],
        "M14": ["M14A", "M14B"],
        "M15": ["M15A", "M15B"],
        "M16": ["M16A", "M16B", "M16E"],
        "R3": ["R3", "R4"]
    }

    # Flatten the fab names for selection
    all_fab_names = []
    for fac_id, fab_list in facility_mapping.items():
        all_fab_names.extend(fab_list)

    # Equipment IDs and models from project knowledge
    hitachi_eqp_ids = [f"ECXDX{random.randint(100, 999)}" for _ in range(10)] + \
                      [f"ECDX{random.randint(100, 999)}" for _ in range(8)] + \
                      [f"HCDX{random.randint(100, 999)}" for _ in range(7)]

    amat_eqp_ids = [f"PCD{random.randint(100, 999)}" for _ in range(8)] + \
                   [f"MCD{random.randint(100, 999)}" for _ in range(7)] + \
                   [f"ACD{random.randint(100, 999)}" for _ in range(6)] + \
                   [f"VCD{random.randint(100, 999)}" for _ in range(4)]

    all_eqp_ids = hitachi_eqp_ids + amat_eqp_ids

    hitachi_models = ['CG6300', 'CG6320', 'CG6340', 'CG6360', 'CG6380']
    amat_models = ['TP3000', 'TP3500', 'TP4000', 'TP4500', 'PROVISION_10', 'PROVISION_20', 'VERITYSEM_4', 'VERITYSEM_5']

    # CD-SEM specific measurement classes and recipes
    classes = ['CD', 'OVL', 'PROF', 'ROUGH', 'THICK', 'GATE', 'CONTACT', 'VIA', 'METAL']

    recipes = {
        'CD': ['CD_GATE_28nm', 'CD_CONTACT_14nm', 'CD_VIA_7nm', 'CD_METAL1_5nm'],
        'OVL': ['OVL_M1M2', 'OVL_GATE_CONTACT', 'OVL_VIA_METAL'],
        'PROF': ['PROF_GATE_SIDEWALL', 'PROF_CONTACT_DEPTH', 'PROF_VIA_TAPER'],
        'ROUGH': ['ROUGH_GATE_LWR', 'ROUGH_SIDEWALL_LER'],
        'THICK': ['THICK_OXIDE', 'THICK_NITRIDE', 'THICK_POLY'],
        'GATE': ['GATE_CD_28nm', 'GATE_PROFILE_3D'],
        'CONTACT': ['CONTACT_CD_14nm', 'CONTACT_DEPTH'],
        'VIA': ['VIA_CD_7nm', 'VIA_TAPER_ANGLE'],
        'METAL': ['METAL1_CD', 'METAL2_PITCH', 'METAL3_WIDTH']
    }

    # Lot ID patterns
    lot_prefixes = ['WF', 'TK', 'DV', 'PD', 'QA', 'EN']

    data = []

    for i in range(n_rows):
        # Select equipment and corresponding model
        eqp_id = random.choice(all_eqp_ids)

        if any(prefix in eqp_id for prefix in ['ECXDX', 'ECDX', 'HCDX']):
            model = random.choice(hitachi_models)
        else:
            model = random.choice(amat_models)

        # Select fab location from actual facility mapping
        fab = random.choice(all_fab_names)

        # Generate lot ID
        lot_id = f"{random.choice(lot_prefixes)}{random.randint(100000, 999999)}"

        # Select class and recipe
        class_name = random.choice(classes)
        recipe = random.choice(recipes[class_name])
        full_name = f"{class_name}/{recipe}"

        # Generate timestamps (within last 30 days)
        days_ago = random.randint(0, 30)
        base_time = datetime.now() - timedelta(days=days_ago)

        # Add some hours/minutes variation
        timestamp = base_time + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        # Measurement duration (typically 5-60 minutes for CD-SEM)
        meas_duration = random.randint(300, 3600)  # 5-60 minutes in seconds
        start_time = timestamp
        end_time = start_time + timedelta(seconds=meas_duration)

        # Generate MSR (unique measurement ID)
        msr_date = start_time.strftime('%Y%m%d')
        msr = f"{msr_date}_{recipe}_{lot_id}"

        # MSR Check (95% success rate)
        msr_check = "Yes" if random.random() < 0.95 else "No"

        # Alignment failure (10% fail rate, 5% unknown)
        align_rand = random.random()
        if align_rand < 0.10:
            align_fail = "Fail"
        elif align_rand < 0.15:
            align_fail = "None"
        else:
            align_fail = "Pass"

        # Image counts and fail ratio
        total_images = random.randint(50, 500)  # Typical range for CD-SEM measurements

        # Fail ratio depends on alignment and other factors
        if align_fail == "Fail" or msr_check == "No":
            fail_ratio = random.uniform(0.15, 0.8)  # Higher fail rate
        else:
            fail_ratio = random.uniform(0.0, 0.15)  # Normal fail rate

        fail_images = int(total_images * fail_ratio)
        actual_fail_ratio = fail_images / total_images if total_images > 0 else 0

        # Recipe file names (tool-specific paths)
        idp_name = f"/Recipe/{class_name}/{recipe}.idp"
        idw_name = f"/Recipe/{class_name}/{recipe}.idw"

        # Add row to data
        data.append({
            'Fab': fab,
            'eqp_id': eqp_id,
            'Tool': eqp_id,  # Legacy column, same as eqp_id
            'Model': model,
            'LotID': lot_id,
            'Timestamp': timestamp,
            'FullName': full_name,
            'Class': class_name,
            'Recipe': recipe,
            'Start_Time': start_time,
            'End_Time': end_time,
            'MSR': msr,
            'MeasTime': meas_duration,
            'MSR_Check': msr_check,
            'Align_fail': align_fail,
            'fail_images': fail_images,
            'total_images': total_images,
            'fail_ratio': round(actual_fail_ratio, 4),
            'idp_name': idp_name,
            'idw_name': idw_name
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Set appropriate data types
    df['Fab'] = df['Fab'].astype('string')
    df['eqp_id'] = df['eqp_id'].astype('string')
    df['Tool'] = df['Tool'].astype('string')
    df['Model'] = df['Model'].astype('string')
    df['LotID'] = df['LotID'].astype('string')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['FullName'] = df['FullName'].astype('string')
    df['Class'] = df['Class'].astype('string')
    df['Recipe'] = df['Recipe'].astype('string')
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])
    df['MSR'] = df['MSR'].astype('string')
    df['MeasTime'] = df['MeasTime'].astype('int64')
    df['MSR_Check'] = df['MSR_Check'].astype('string')
    df['Align_fail'] = df['Align_fail'].astype('string')
    df['fail_images'] = df['fail_images'].astype('int64')
    df['total_images'] = df['total_images'].astype('int64')
    df['fail_ratio'] = df['fail_ratio'].astype('float64')
    df['idp_name'] = df['idp_name'].astype('string')
    df['idw_name'] = df['idw_name'].astype('string')

    return df


# Generate the dummy data
print("Generating CD-SEM Measurement History dummy data...")
meas_hist_df = generate_meas_hist_dummy_data(n_rows=500)

# Display basic information
print(f"\nGenerated DataFrame with {len(meas_hist_df)} rows")
print("\nFirst 5 rows:")
print(meas_hist_df.head())

print("\nDataFrame Info:")
print(meas_hist_df.info())

print("\nSample statistics:")
print(f"Unique equipment count: {meas_hist_df['eqp_id'].nunique()}")
print(f"Unique lot count: {meas_hist_df['LotID'].nunique()}")
print(f"Date range: {meas_hist_df['Timestamp'].min()} to {meas_hist_df['Timestamp'].max()}")

print("\nClass distribution:")
print(meas_hist_df['Class'].value_counts())

print("\nMSR Check distribution:")
print(meas_hist_df['MSR_Check'].value_counts())

print("\nAlignment failure distribution:")
print(meas_hist_df['Align_fail'].value_counts())

print(f"\nAverage measurement time: {meas_hist_df['MeasTime'].mean():.1f} seconds")
print(f"Average fail ratio: {meas_hist_df['fail_ratio'].mean():.4f}")

# Convert to records format for web application
print("\n" + "=" * 50)
print("DATA FOR WEB APPLICATION (to_dict('records') format)")
print("=" * 50)

# Convert to records format (first 3 records as example)
records_data = meas_hist_df.head(3).to_dict('records')
print("Sample of records format (first 3 rows):")
for i, record in enumerate(records_data, 1):
    print(f"\nRecord {i}:")
    for key, value in record.items():
        print(f"  {key}: {value}")

print(f"\nTotal records available: {len(meas_hist_df)}")
print("Use meas_hist_df.to_dict('records') to get all data in web application format")

# Save to CSV for reference
import os

folder_path = 'sample_data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

csv_filename = os.path.join(folder_path, 'meas_hist_dummy_data.csv')
meas_hist_df.to_csv(csv_filename, index=False)
print(f"\nData also saved to: {csv_filename}")