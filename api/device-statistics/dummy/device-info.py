import random
import string
import pprint


def generate_dummy_row(row_id):
    """
    Generates a single row of dummy data as a dictionary.

    Args:
        row_id (int): A unique ID to ensure recipe_id and oper_id are unique.

    Returns:
        dict: A dictionary representing a single row of data.
    """
    # --- Define possible values for columns ---

    # Select from 10 predefined 4-letter product IDs
    prod_ids = ['PROA', 'PROB', 'PROC', 'PROD', 'PROE',
                'PROF', 'PROG', 'PROH', 'PROI', 'PROJ']

    # Sample operation descriptions
    oper_descriptions = [
        'Initial Material Prep', 'Primary Etching', 'Deposition Layer 1',
        'Photolithography', 'Ion Implantation', 'Chemical Cleaning',
        'Annealing Process', 'Final Inspection', 'Wafer Testing'
    ]

    # --- Generate random data for each column ---

    prod_id = random.choice(prod_ids)
    oper_id = f"OPER-{1000 + row_id}"
    oper_desc = random.choice(oper_descriptions)
    recipe_id = f"RCP-{prod_id}-{500 + row_id}"

    # Generate numeric values
    para_all = random.randint(500, 1000)
    para_16 = random.randint(100, para_all // 2)
    para_13 = random.randint(50, para_all // 3)
    para_9 = random.randint(20, para_all // 4)
    para_5 = random.randint(10, para_all // 5)

    # --- Helper function for percentage calculation ---
    def calculate_percent(part, total):
        if total == 0:
            return 0.0
        return round((part / total) * 100, 2)

    # --- Construct the row dictionary ---
    row = {
        "prod_id": prod_id,
        "oper_id": oper_id,
        "oper_desc": oper_desc,
        "oper_seq": random.randint(1, 10),
        "samp_seq": random.randint(1, 5),
        "eqp_id": f"EQP-{''.join(random.choices(string.ascii_uppercase + string.digits, k=3))}",
        "recipe_id": recipe_id,
        "bak_eqp_id_ival": f"BAK-{''.join(random.choices(string.ascii_uppercase + string.digits, k=3))}",
        "skip_yn": random.choice(["Yes", "No"]),
        "chg_tm": f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}",
        "ctn_desc": f"Container for {prod_id}",
        "para_all": para_all,
        "para_16": para_16,
        "para_13": para_13,
        "para_9": para_9,
        "para_5": para_5,
        "para_16_percent": calculate_percent(para_16, para_all),
        "para_13_percent": calculate_percent(para_13, para_all),
        "para_9_percent": calculate_percent(para_9, para_all),
        "para_5_percent": calculate_percent(para_5, para_all),
    }
    return row


def generate_summary_row(prod_id):
    """
    Generates a single row of summary data for a given product ID.

    Args:
        prod_id (str): The product ID to generate a summary for.

    Returns:
        dict: A dictionary representing a single row of summary data.
    """
    # --- Generate summary numeric values ---
    # These represent aggregated values (e.g., averages or sums) across all recipes for a product.
    para_all = random.randint(5000, 10000)
    para_16 = random.randint(1000, para_all // 2)
    para_13 = random.randint(500, para_all // 3)
    para_9 = random.randint(200, para_all // 4)
    para_5 = random.randint(100, para_all // 5)

    # --- Generate recipe availability stats ---
    total_recipe = random.randint(20, 50)
    # Ensure available recipes are less than or equal to the total
    avail_recipe = random.randint(10, total_recipe)

    # --- Helper function for percentage calculation ---
    def calculate_percent(part, total):
        if total == 0:
            return 0.0
        return round((part / total) * 100, 2)

    # --- Construct the summary row dictionary ---
    row = {
        "prod_id": prod_id,
        "para_all": para_all,
        "para_16": para_16,
        "para_13": para_13,
        "para_9": para_9,
        "para_5": para_5,
        "para_16_percent": calculate_percent(para_16, para_all),
        "para_13_percent": calculate_percent(para_13, para_all),
        "para_9_percent": calculate_percent(para_9, para_all),
        "para_5_percent": calculate_percent(para_5, para_all),
        "ctn_desc": f"Summary Container for {prod_id}",
        "total_recipe": total_recipe,
        "avail_recipe": avail_recipe,
        "avail_recipe_percent": calculate_percent(avail_recipe, total_recipe)
    }
    return row


def get_category(meas_counting):
    """
    Determines the category based on the measurement counting value.

    Args:
        meas_counting (int): The number of measurement points.

    Returns:
        str: The corresponding category name.
    """
    if 1 <= meas_counting <= 5:
        return "para_5"
    elif 6 <= meas_counting <= 9:
        return "para_9"
    elif 10 <= meas_counting <= 13:
        return "para_13"
    elif meas_counting >= 14:
        return "para_16"
    else:
        return "undefined"


def generate_recipe_parameter(prod_id, recipe_id, param_index):
    """
    Generates a single row of recipe parameter data.

    Args:
        prod_id (str): The product ID.
        recipe_id (str): The recipe ID.
        param_index (int): An index to make parameter names unique.

    Returns:
        dict: A dictionary representing a single parameter row.
    """
    # --- Define possible parameter names ---
    param_prefixes = ["Temp", "Pressure", "GasFlow", "Voltage", "Duration", "RF_Power"]
    param_suffixes = ["Zone1", "ChamberA", "Step2", "N2", "Ar", "Main"]
    parameter_name = f"{random.choice(param_prefixes)}_{random.choice(param_suffixes)}_{param_index}"

    # --- Generate random data for the row ---
    meas_counting = random.randint(1, 25)
    category = get_category(meas_counting)

    # Let's assume about 1 in 5 parameters is a "Mother" parameter
    is_mother = random.choice([True, False, False, False, False])

    row = {
        "Parameter": parameter_name,
        "Mother_Para": is_mother,
        "Meas_Counting": meas_counting,
        "prod_id": prod_id,
        "recipe_id": recipe_id,
        "modified": random.choice([True, False]),
        "category": category,
    }
    return row


def generate_working_device_row(lot_cd):
    """
    Generates a single row of working device data.

    Args:
        lot_cd (str): The lot code, which corresponds to a product ID.

    Returns:
        dict: A dictionary representing a single working device.
    """
    # --- Define the possible product categories ---
    product_categories = ["DRAM", "NAND", "NM"]

    # --- Construct the row dictionary ---
    row = {
        "lot_cd": lot_cd,
        "prod_catg_cd2": random.choice(product_categories)
    }
    return row


def get_r3_options():
    """
    Returns the three R3 facility options.
    
    Returns:
        list: List of R3 options ["DRAM", "NAND", "NM"]
    """
    return ["DRAM", "NAND", "NM"]


def get_device_names():
    """
    Returns a list of random device names for non-R3 facilities.
    
    Returns:
        list: List of 10 random device names
    """
    device_names = [
        "DEV-Alpha-001",
        "DEV-Beta-002", 
        "DEV-Gamma-003",
        "DEV-Delta-004",
        "DEV-Epsilon-005",
        "DEV-Zeta-006",
        "DEV-Eta-007",
        "DEV-Theta-008",
        "DEV-Iota-009",
        "DEV-Kappa-010"
    ]
    return device_names


def get_r3_data(option):
    """
    Returns device statistics data for R3 facility based on selected option.
    
    Args:
        option (str): Selected R3 option ("DRAM", "NAND", or "NM")
        
    Returns:
        dict: Device statistics data for the selected R3 option
    """
    if option not in ["DRAM", "NAND", "NM"]:
        return {"error": "Invalid R3 option"}
    
    # Generate sample data based on option
    base_data = []
    for i in range(20):
        row = generate_dummy_row(i)
        row["facility"] = "R3"
        row["option_type"] = option
        row["device_category"] = option
        base_data.append(row)
    
    return {
        "option": option,
        "facility": "R3",
        "data": base_data,
        "summary": generate_summary_row(f"R3_{option}")
    }


def get_device_data(device_name):
    """
    Returns device statistics data for a specific device name.
    
    Args:
        device_name (str): Selected device name
        
    Returns:
        dict: Device statistics data for the selected device
    """
    if not device_name:
        return {"error": "Device name is required"}
    
    # Generate sample data for the device
    base_data = []
    for i in range(15):
        row = generate_dummy_row(i)
        row["device_name"] = device_name
        row["facility"] = "Non-R3"
        base_data.append(row)
    
    return {
        "device_name": device_name,
        "facility": "Non-R3",
        "data": base_data,
        "summary": generate_summary_row(device_name)
    }


def get_all_data():
    """
    Returns all device statistics data (legacy function).
    
    Returns:
        dict: All device statistics data
    """
    return {
        "all_rcp_info": [generate_dummy_row(i) for i in range(100)],
        "only_normal_rcp_info": [generate_dummy_row(i) for i in range(100, 180)],
        "mother_normal_rcp_info": [generate_dummy_row(i) for i in range(180, 230)],
        "only_sample_rcp_info": [generate_dummy_row(i) for i in range(230, 260)]
    }



# --- Main script execution ---
if __name__ == "__main__":
    # Generate data for each category. We use a global counter to ensure all IDs are unique across lists.
    unique_id_counter = 0

    all_rcp_data = []
    for i in range(100):  # Generate 100 rows
        all_rcp_data.append(generate_dummy_row(unique_id_counter))
        unique_id_counter += 1

    only_normal_rcp_data = []
    for i in range(80):  # Generate 80 rows
        only_normal_rcp_data.append(generate_dummy_row(unique_id_counter))
        unique_id_counter += 1

    mother_normal_rcp_data = []
    for i in range(50):  # Generate 50 rows
        mother_normal_rcp_data.append(generate_dummy_row(unique_id_counter))
        unique_id_counter += 1

    only_sample_rcp_data = []
    for i in range(30):  # Generate 30 rows
        only_sample_rcp_data.append(generate_dummy_row(unique_id_counter))
        unique_id_counter += 1

    # Create the final dictionary containing all the generated data lists
    # As requested, the keys are the names of your data sets.
    data_dictionary = {
        "all_rcp_info": all_rcp_data,
        "only_normal_rcp_info": only_normal_rcp_data,
        "mother_normal_rcp_info": mother_normal_rcp_data,
        "only_sample_rcp_info": only_sample_rcp_data
    }

    # --- Print a sample of the generated data ---
    print("--- Sample from 'all_rcp_info' ---")
    pprint.pprint(data_dictionary["all_rcp_info"][0])
    print(f"\nTotal rows in 'all_rcp_info': {len(data_dictionary['all_rcp_info'])}")

    print("\n--- Sample from 'only_normal_rcp_info' ---")
    pprint.pprint(data_dictionary["only_normal_rcp_info"][0])
    print(f"\nTotal rows in 'only_normal_rcp_info': {len(data_dictionary['only_normal_rcp_info'])}")

    # --- Example: How to load into pandas DataFrames ---
    try:
        import pandas as pd

        # You can easily convert these lists of dictionaries into pandas DataFrames
        all_rcp_df = pd.DataFrame(data_dictionary["all_rcp_info"])
        only_normal_rcp_df = pd.DataFrame(data_dictionary["only_normal_rcp_info"])
        mother_normal_rcp_df = pd.DataFrame(data_dictionary["mother_normal_rcp_info"])
        only_sample_rcp_df = pd.DataFrame(data_dictionary["only_sample_rcp_info"])

        print("\n--- Successfully converted to pandas DataFrames ---")
        print("\nHead of 'all_rcp_df':")
        print(all_rcp_df.head())

    except ImportError:
        print("\n--- pandas is not installed. Skipping DataFrame conversion example. ---")
        print("To install pandas, run: pip install pandas")

