import pandas as pd
import numpy as np
import random
from datetime import datetime
import hashlib


def generate_msr_data_from_csv(meas_hist_csv_path, seed_offset=0):
    """
    Generate MSR measurement data from saved measurement history CSV file
    This ensures consistent data generation for Flask server

    Parameters:
    meas_hist_csv_path: path to the measurement history CSV file
    seed_offset: offset for random seed to generate different variations if needed
    """

    # Read measurement history data from CSV
    try:
        meas_hist_df = pd.read_csv(meas_hist_csv_path)
        print(f"Loaded {len(meas_hist_df)} measurement history records from CSV")
    except FileNotFoundError:
        print(f"Error: Could not find {meas_hist_csv_path}")
        return None

    # Measurement parameters by class type
    parameter_mapping = {
        'CD': ['CD_TOP', 'CD_BOTTOM', 'CD_MIDDLE', 'SIDEWALL_ANGLE'],
        'OVL': ['OVERLAY_X', 'OVERLAY_Y', 'OVERLAY_R', 'OVERLAY_THETA'],
        'PROF': ['HEIGHT', 'SIDEWALL_ANGLE', 'TOP_WIDTH', 'BOTTOM_WIDTH'],
        'ROUGH': ['LWR', 'LER', 'RMS_ROUGHNESS', 'CORRELATION_LENGTH'],
        'THICK': ['THICKNESS', 'UNIFORMITY', 'REFRACTIVE_INDEX'],
        'GATE': ['GATE_CD', 'GATE_HEIGHT', 'GATE_PROFILE'],
        'CONTACT': ['CONTACT_CD', 'CONTACT_DEPTH', 'ASPECT_RATIO'],
        'VIA': ['VIA_CD', 'VIA_DEPTH', 'TAPER_ANGLE'],
        'METAL': ['LINE_WIDTH', 'LINE_HEIGHT', 'PITCH', 'SPACE_WIDTH']
    }

    # Generate chip positions for a typical wafer (simplified grid)
    chip_positions = []
    for x in range(-10, 11):  # -10 to 10
        for y in range(-10, 11):  # -10 to 10
            # Skip corner positions (realistic wafer shape)
            if abs(x) + abs(y) <= 15:
                chip_positions.append((x, y))

    all_msr_data = []

    for idx, meas_record in meas_hist_df.iterrows():
        msr = meas_record['MSR']
        class_name = meas_record['Class']
        total_images = meas_record['total_images']

        # Use MSR as seed for consistent generation per measurement
        # This ensures same MSR always generates same measurement data
        msr_seed = int(hashlib.md5(msr.encode()).hexdigest()[:8], 16) + seed_offset
        np.random.seed(msr_seed % (2 ** 31))  # Ensure seed is within valid range
        random.seed(msr_seed % (2 ** 31))

        # Determine number of measurement points (consistent per MSR)
        num_measurements = min(random.randint(20, 80), total_images // 2)

        # Select parameters for this measurement class
        available_params = parameter_mapping.get(class_name, ['WAFER', 'EDGE', 'LEVEL'])
        num_params = min(random.randint(1, 3), len(available_params))
        selected_params = random.sample(available_params, num_params)

        # Generate measurements for each sequence
        for sequence in range(1, num_measurements + 1):
            # Select chip position (consistent pattern per MSR)
            chip_idx = (sequence - 1) % len(chip_positions)
            chip_x, chip_y = chip_positions[chip_idx]
            chip_number = f"{chip_x}, {chip_y}"

            # Generate coordinates (deterministic based on sequence and MSR)
            base_chip_coord = 12000000 + (sequence * 1000) + (msr_seed % 1000000)
            base_chip_coord_y = 250000 + (sequence * 100)
            chip_coordinate = f"{base_chip_coord},{base_chip_coord_y}"

            base_stage_x = 175000000 + (sequence * 10000) + (msr_seed % 100000)
            base_stage_y = 147000000 + (sequence * 5000)
            stage_coordinate = f"{base_stage_x}, {base_stage_y}"

            # Generate dnum_group (measurement point group)
            if sequence % 20 == 0:  # Every 20th measurement has no data
                dnum_group = "-1, -1"
                mp_number = -1
            else:
                mp_x = (sequence - 1) % 30  # Cycle through 0-29
                dnum_group = f"{mp_x}, -1"  # y is always -1
                mp_number = mp_x

            # Generate measurement data for each parameter
            for param_idx, param in enumerate(selected_params):
                # Generate realistic CD values based on parameter type (deterministic)
                param_seed = msr_seed + sequence + param_idx * 1000
                np.random.seed(param_seed % (2 ** 31))

                if 'CD' in param or 'WIDTH' in param:
                    cd_value = round(np.random.uniform(15.0, 45.0), 2)  # nm range
                elif 'HEIGHT' in param or 'DEPTH' in param:
                    cd_value = round(np.random.uniform(50.0, 200.0), 2)  # nm range
                elif 'ANGLE' in param:
                    cd_value = round(np.random.uniform(85.0, 95.0), 2)  # degrees
                elif 'OVERLAY' in param:
                    cd_value = round(np.random.uniform(-5.0, 5.0), 2)  # nm range
                elif 'ROUGH' in param:
                    cd_value = round(np.random.uniform(1.0, 5.0), 2)  # nm range
                elif 'THICK' in param:
                    cd_value = round(np.random.uniform(10.0, 100.0), 2)  # nm range
                else:
                    cd_value = round(np.random.uniform(10.0, 50.0), 2)  # default range

                # Number of images for this measurement point
                no_of_mp_image = 1 + (param_seed % 5)  # 1-5 images

                # Generate image file name (deterministic)
                mp_image_name_01 = f"{msr}_{sequence:03d}_{param}_{param_seed % 10000:04d}.tif"

                # Add measurement record
                all_msr_data.append({
                    'MSR': msr,
                    'sequence': sequence,
                    'chip_number': chip_number,
                    'chip_coordinate': chip_coordinate,
                    'stage_coordinate': stage_coordinate,
                    'dnum_group': dnum_group,
                    'mp_number': mp_number,
                    'parameter': param,
                    'cd_value': cd_value,
                    'no_of_mp_image': no_of_mp_image,
                    'mp_image_name_01': mp_image_name_01
                })

    # Create DataFrame
    msr_df = pd.DataFrame(all_msr_data)

    # Set appropriate data types
    msr_df['MSR'] = msr_df['MSR'].astype('string')
    msr_df['sequence'] = msr_df['sequence'].astype('int64')
    msr_df['chip_number'] = msr_df['chip_number'].astype('string')
    msr_df['chip_coordinate'] = msr_df['chip_coordinate'].astype('string')
    msr_df['stage_coordinate'] = msr_df['stage_coordinate'].astype('string')
    msr_df['dnum_group'] = msr_df['dnum_group'].astype('string')
    msr_df['mp_number'] = msr_df['mp_number'].astype('int64')
    msr_df['parameter'] = msr_df['parameter'].astype('string')
    msr_df['cd_value'] = msr_df['cd_value'].astype('float64')
    msr_df['no_of_mp_image'] = msr_df['no_of_mp_image'].astype('int64')
    msr_df['mp_image_name_01'] = msr_df['mp_image_name_01'].astype('string')

    return msr_df


def get_msr_data_for_msr_id(msr_id, meas_hist_csv_path):
    """
    Get MSR measurement data for a specific MSR ID
    Useful for Flask API endpoints
    """
    # Read measurement history to verify MSR exists
    meas_hist_df = pd.read_csv(meas_hist_csv_path)

    if msr_id not in meas_hist_df['MSR'].values:
        return None

    # Get the specific measurement record
    meas_record = meas_hist_df[meas_hist_df['MSR'] == msr_id].iloc[0]

    # Generate MSR data for just this MSR (same logic as above but for single MSR)
    class_name = meas_record['Class']
    total_images = meas_record['total_images']

    # Use MSR as seed for consistent generation
    msr_seed = int(hashlib.md5(msr_id.encode()).hexdigest()[:8], 16)
    np.random.seed(msr_seed % (2 ** 31))
    random.seed(msr_seed % (2 ** 31))

    parameter_mapping = {
        'CD': ['CD_TOP', 'CD_BOTTOM', 'CD_MIDDLE', 'SIDEWALL_ANGLE'],
        'OVL': ['OVERLAY_X', 'OVERLAY_Y', 'OVERLAY_R', 'OVERLAY_THETA'],
        'PROF': ['HEIGHT', 'SIDEWALL_ANGLE', 'TOP_WIDTH', 'BOTTOM_WIDTH'],
        'ROUGH': ['LWR', 'LER', 'RMS_ROUGHNESS', 'CORRELATION_LENGTH'],
        'THICK': ['THICKNESS', 'UNIFORMITY', 'REFRACTIVE_INDEX'],
        'GATE': ['GATE_CD', 'GATE_HEIGHT', 'GATE_PROFILE'],
        'CONTACT': ['CONTACT_CD', 'CONTACT_DEPTH', 'ASPECT_RATIO'],
        'VIA': ['VIA_CD', 'VIA_DEPTH', 'TAPER_ANGLE'],
        'METAL': ['LINE_WIDTH', 'LINE_HEIGHT', 'PITCH', 'SPACE_WIDTH']
    }

    chip_positions = []
    for x in range(-10, 11):
        for y in range(-10, 11):
            if abs(x) + abs(y) <= 15:
                chip_positions.append((x, y))

    num_measurements = min(random.randint(20, 80), total_images // 2)
    available_params = parameter_mapping.get(class_name, ['WAFER', 'EDGE', 'LEVEL'])
    num_params = min(random.randint(1, 3), len(available_params))
    selected_params = random.sample(available_params, num_params)

    msr_data = []

    for sequence in range(1, num_measurements + 1):
        chip_idx = (sequence - 1) % len(chip_positions)
        chip_x, chip_y = chip_positions[chip_idx]
        chip_number = f"{chip_x}, {chip_y}"

        base_chip_coord = 12000000 + (sequence * 1000) + (msr_seed % 1000000)
        base_chip_coord_y = 250000 + (sequence * 100)
        chip_coordinate = f"{base_chip_coord},{base_chip_coord_y}"

        base_stage_x = 175000000 + (sequence * 10000) + (msr_seed % 100000)
        base_stage_y = 147000000 + (sequence * 5000)
        stage_coordinate = f"{base_stage_x}, {base_stage_y}"

        if sequence % 20 == 0:
            dnum_group = "-1, -1"
            mp_number = -1
        else:
            mp_x = (sequence - 1) % 30
            dnum_group = f"{mp_x}, -1"
            mp_number = mp_x

        for param_idx, param in enumerate(selected_params):
            param_seed = msr_seed + sequence + param_idx * 1000
            np.random.seed(param_seed % (2 ** 31))

            if 'CD' in param or 'WIDTH' in param:
                cd_value = round(np.random.uniform(15.0, 45.0), 2)
            elif 'HEIGHT' in param or 'DEPTH' in param:
                cd_value = round(np.random.uniform(50.0, 200.0), 2)
            elif 'ANGLE' in param:
                cd_value = round(np.random.uniform(85.0, 95.0), 2)
            elif 'OVERLAY' in param:
                cd_value = round(np.random.uniform(-5.0, 5.0), 2)
            elif 'ROUGH' in param:
                cd_value = round(np.random.uniform(1.0, 5.0), 2)
            elif 'THICK' in param:
                cd_value = round(np.random.uniform(10.0, 100.0), 2)
            else:
                cd_value = round(np.random.uniform(10.0, 50.0), 2)

            no_of_mp_image = 1 + (param_seed % 5)
            mp_image_name_01 = f"{msr_id}_{sequence:03d}_{param}_{param_seed % 10000:04d}.tif"

            msr_data.append({
                'MSR': msr_id,
                'sequence': sequence,
                'chip_number': chip_number,
                'chip_coordinate': chip_coordinate,
                'stage_coordinate': stage_coordinate,
                'dnum_group': dnum_group,
                'mp_number': mp_number,
                'parameter': param,
                'cd_value': cd_value,
                'no_of_mp_image': no_of_mp_image,
                'mp_image_name_01': mp_image_name_01
            })

    return pd.DataFrame(msr_data)


# Example usage:
if __name__ == "__main__":
    # Path to your measurement history CSV file
    csv_path = 'sample_data/meas_hist_dummy_data.csv'

    print("Generating MSR data from CSV file...")

    # Generate all MSR data from CSV
    msr_df = generate_msr_data_from_csv(csv_path)

    if msr_df is not None:
        print(f"\nGenerated {len(msr_df)} MSR measurement records")
        print(f"Unique MSR count: {msr_df['MSR'].nunique()}")

        print("\nFirst 5 rows:")
        print(msr_df.head())

        print("\nParameter distribution:")
        print(msr_df['parameter'].value_counts())

        # Save MSR data to CSV
        import os

        folder_path = 'sample_data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        msr_csv_path = os.path.join(folder_path, 'msr_dummy_data_from_csv.csv')
        msr_df.to_csv(msr_csv_path, index=False)
        print(f"\nMSR data saved to: {msr_csv_path}")

        # Example: Get data for specific MSR
        sample_msr = msr_df['MSR'].iloc[0]
        print(f"\nTesting single MSR lookup for: {sample_msr}")

        single_msr_data = get_msr_data_for_msr_id(sample_msr, csv_path)
        if single_msr_data is not None:
            print(f"Found {len(single_msr_data)} records for MSR: {sample_msr}")

            # Convert to records format for web application
            records_data = single_msr_data.to_dict('records')
            print(f"\nSample records format (first 2 records):")
            for i, record in enumerate(records_data[:2], 1):
                print(f"\nRecord {i}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("FLASK SERVER INTEGRATION EXAMPLE")
    print("=" * 60)
    print("""
# In your Flask server:

from your_module import generate_msr_data_from_csv, get_msr_data_for_msr_id

# Load measurement history data
@app.route('/api/measurements')
def get_measurements():
    meas_hist_df = pd.read_csv('sample_data/meas_hist_dummy_data.csv')
    return meas_hist_df.to_dict('records')

# Get MSR details for specific measurement
@app.route('/api/msr/<msr_id>')
def get_msr_details(msr_id):
    msr_data = get_msr_data_for_msr_id(msr_id, 'sample_data/meas_hist_dummy_data.csv')
    if msr_data is not None:
        return msr_data.to_dict('records')
    else:
        return {'error': 'MSR not found'}, 404
    """)