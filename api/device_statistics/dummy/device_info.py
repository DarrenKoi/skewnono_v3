import random
import string
import pprint
from datetime import datetime, timedelta
import pandas as pd


def generate_dummy_row(row_id):
    """
    Generates a single row of dummy data as a dictionary.

    Args:
        row_id (int): A unique ID to ensure recipe_id and oper_id are unique.

    Returns:
        dict: A dictionary representing a single row of data.
    """
    # --- Define possible values for columns ---

    # Select from 40 predefined 4-letter product IDs
    prod_ids = [
        # DRAM products (15)
        'PROA', 'PROB', 'PROC', 'PROK', 'PROL', 'PROM', 'PRON', 'PROO', 
        'PROP', 'PROQ', 'PROR', 'PROS', 'PROT', 'PROU', 'PROV',
        # NAND products (15)
        'PROD', 'PROE', 'PROF', 'PROG', 'PROW', 'PROX', 'PROY', 'PROZ',
        'PR1A', 'PR1B', 'PR1C', 'PR1D', 'PR1E', 'PR1F', 'PR1G',
        # NM products (10)
        'PROH', 'PROI', 'PROJ', 'PR2A', 'PR2B', 'PR2C', 'PR2D', 'PR2E', 
        'PR2F', 'PR2G'
    ]

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
    Returns the three R3 facility options with their associated product IDs.
    
    Returns:
        dict: Dictionary containing devices with categories and their prod_ids
    """
    return {
        "devices": [
            {
                "category": "DRAM",
                "prod_ids": [
                    'PROA', 'PROB', 'PROC', 'PROK', 'PROL', 'PROM', 'PRON', 'PROO',
                    'PROP', 'PROQ', 'PROR', 'PROS', 'PROT', 'PROU', 'PROV'
                ]
            },
            {
                "category": "NAND", 
                "prod_ids": [
                    'PROD', 'PROE', 'PROF', 'PROG', 'PROW', 'PROX', 'PROY', 'PROZ',
                    'PR1A', 'PR1B', 'PR1C', 'PR1D', 'PR1E', 'PR1F', 'PR1G'
                ]
            },
            {
                "category": "NM",
                "prod_ids": [
                    'PROH', 'PROI', 'PROJ', 'PR2A', 'PR2B', 'PR2C', 'PR2D', 'PR2E',
                    'PR2F', 'PR2G'
                ]
            }
        ]
    }


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


def get_r3_data(option, prod_ids=None):
    """
    Returns device statistics data for R3 facility based on selected option with weekly structure.
    
    Args:
        option (str): Selected R3 option ("DRAM", "NAND", or "NM")
        prod_ids (list): Optional list of specific product IDs to filter by
        
    Returns:
        dict: Device statistics data for the selected R3 option organized by week
    """
    options = get_r3_options()
    
    # Find the category data for the selected option
    category_data = None
    for device in options["devices"]:
        if device["category"] == option:
            category_data = device.copy()
            break
    
    if not category_data:
        return {"error": "Invalid R3 option"}
    
    # Filter prod_ids if specified
    if prod_ids:
        # Only include prod_ids that are both in the request and in the category
        filtered_prod_ids = [pid for pid in prod_ids if pid in category_data["prod_ids"]]
        if not filtered_prod_ids:
            return {"error": "No valid product IDs for this category"}
        category_data["prod_ids"] = filtered_prod_ids
    
    # Generate weekly data for the selected category with filtered prod_ids
    return generate_weekly_data(category_data)


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


def generate_recipe_info_data(prod_ids, num_rows=50):
    """
    Generates recipe info data for given product IDs.
    
    Args:
        prod_ids (list): List of product IDs to use
        num_rows (int): Number of rows to generate
        
    Returns:
        dict: Recipe info data categorized by type, including recipe_ids for matching
    """
    rcp_info = {
        "all_rcp_info": [],
        "only_normal_rcp_info": [],
        "mother_normal_rcp_info": [],
        "only_sample_rcp_info": [],
        "all_recipe_ids": []  # Track all recipe IDs for use in all_recipe_list
    }
    
    # Generate rows for each category
    for i in range(num_rows):
        row = generate_dummy_row(i)
        row['prod_id'] = random.choice(prod_ids)
        
        # Collect all recipe IDs
        rcp_info["all_recipe_ids"].append(row['recipe_id'])
        
        # Distribute across different categories
        if i % 4 == 0:
            rcp_info["all_rcp_info"].append(row)
        elif i % 4 == 1:
            rcp_info["only_normal_rcp_info"].append(row)
        elif i % 4 == 2:
            rcp_info["mother_normal_rcp_info"].append(row)
        else:
            rcp_info["only_sample_rcp_info"].append(row)
    
    return rcp_info


def generate_summary_data_by_category(prod_ids):
    """
    Generates summary data for each category (all, only_normal, mother_normal, only_sample).
    
    Args:
        prod_ids (list): List of product IDs
        
    Returns:
        dict: Summary data for each category
    """
    summary_data = {
        "all_summary": [],
        "only_normal_summary": [],
        "mother_normal_summary": [],
        "only_sample_summary": []
    }
    
    for prod_id in prod_ids:
        # Generate summary for each category with different value ranges
        
        # All summary - highest values
        all_summary_row = generate_summary_row(prod_id)
        summary_data["all_summary"].append(all_summary_row)
        
        # Only normal summary - medium values
        normal_para_all = random.randint(3000, 7000)
        normal_summary_row = {
            "prod_id": prod_id,
            "para_all": normal_para_all,
            "para_16": random.randint(600, normal_para_all // 2),
            "para_13": random.randint(300, normal_para_all // 3),
            "para_9": random.randint(150, normal_para_all // 4),
            "para_5": random.randint(80, normal_para_all // 5),
            "ctn_desc": f"Normal Container for {prod_id}",
            "total_recipe": random.randint(15, 40),
            "avail_recipe": random.randint(8, 30)
        }
        # Calculate percentages
        normal_summary_row["para_16_percent"] = round((normal_summary_row["para_16"] / normal_para_all) * 100, 2)
        normal_summary_row["para_13_percent"] = round((normal_summary_row["para_13"] / normal_para_all) * 100, 2)
        normal_summary_row["para_9_percent"] = round((normal_summary_row["para_9"] / normal_para_all) * 100, 2)
        normal_summary_row["para_5_percent"] = round((normal_summary_row["para_5"] / normal_para_all) * 100, 2)
        normal_summary_row["avail_recipe_percent"] = round((normal_summary_row["avail_recipe"] / normal_summary_row["total_recipe"]) * 100, 2)
        summary_data["only_normal_summary"].append(normal_summary_row)
        
        # Mother normal summary - lower values
        mother_para_all = random.randint(2000, 5000)
        mother_summary_row = {
            "prod_id": prod_id,
            "para_all": mother_para_all,
            "para_16": random.randint(400, mother_para_all // 2),
            "para_13": random.randint(200, mother_para_all // 3),
            "para_9": random.randint(100, mother_para_all // 4),
            "para_5": random.randint(50, mother_para_all // 5),
            "ctn_desc": f"Mother Container for {prod_id}",
            "total_recipe": random.randint(10, 25),
            "avail_recipe": random.randint(5, 20)
        }
        # Calculate percentages
        mother_summary_row["para_16_percent"] = round((mother_summary_row["para_16"] / mother_para_all) * 100, 2)
        mother_summary_row["para_13_percent"] = round((mother_summary_row["para_13"] / mother_para_all) * 100, 2)
        mother_summary_row["para_9_percent"] = round((mother_summary_row["para_9"] / mother_para_all) * 100, 2)
        mother_summary_row["para_5_percent"] = round((mother_summary_row["para_5"] / mother_para_all) * 100, 2)
        mother_summary_row["avail_recipe_percent"] = round((mother_summary_row["avail_recipe"] / mother_summary_row["total_recipe"]) * 100, 2)
        summary_data["mother_normal_summary"].append(mother_summary_row)
        
        # Only sample summary - lowest values
        sample_para_all = random.randint(1000, 3000)
        sample_summary_row = {
            "prod_id": prod_id,
            "para_all": sample_para_all,
            "para_16": random.randint(200, sample_para_all // 2),
            "para_13": random.randint(100, sample_para_all // 3),
            "para_9": random.randint(50, sample_para_all // 4),
            "para_5": random.randint(25, sample_para_all // 5),
            "ctn_desc": f"Sample Container for {prod_id}",
            "total_recipe": random.randint(5, 15),
            "avail_recipe": random.randint(2, 12)
        }
        # Calculate percentages
        sample_summary_row["para_16_percent"] = round((sample_summary_row["para_16"] / sample_para_all) * 100, 2)
        sample_summary_row["para_13_percent"] = round((sample_summary_row["para_13"] / sample_para_all) * 100, 2)
        sample_summary_row["para_9_percent"] = round((sample_summary_row["para_9"] / sample_para_all) * 100, 2)
        sample_summary_row["para_5_percent"] = round((sample_summary_row["para_5"] / sample_para_all) * 100, 2)
        sample_summary_row["avail_recipe_percent"] = round((sample_summary_row["avail_recipe"] / sample_summary_row["total_recipe"]) * 100, 2)
        summary_data["only_sample_summary"].append(sample_summary_row)
    
    return summary_data


def generate_summary_data(prod_ids):
    """
    Generates summary data for given product IDs.
    
    Args:
        prod_ids (list): List of product IDs
        
    Returns:
        list: List of summary data for each product ID
    """
    summary_data = []
    for prod_id in prod_ids:
        summary_data.append(generate_summary_row(prod_id))
    return summary_data


def generate_all_recipe_list(prod_ids, recipe_ids=None):
    """
    Generates a flattened list of recipe parameters that can be converted to DataFrame.
    
    Args:
        prod_ids (list): List of product IDs
        recipe_ids (list): Optional list of specific recipe IDs to use (for matching with rcp_info)
        
    Returns:
        list: List of parameter dictionaries with columns:
              ["Parameter", "Mother_Para", "Meas_Counting", "prod_id", "recipe_id", "modified", "category"]
    """
    all_parameters = []
    
    # If no recipe_ids provided, generate some default ones
    if recipe_ids is None:
        recipe_ids = []
        for i in range(30):
            prod_id = random.choice(prod_ids)
            recipe_ids.append(f"RCP-{prod_id}-{500 + i}")
    
    # For each recipe, generate parameters
    for recipe_id in recipe_ids:
        # Extract prod_id from recipe_id (format: RCP-{prod_id}-{number})
        # Handle cases where prod_id might contain dashes
        parts = recipe_id.split('-')
        if len(parts) >= 3:
            prod_id = parts[1]  # Standard format: RCP-PROA-500
        else:
            # Fallback: use a random prod_id from the list
            prod_id = random.choice(prod_ids)
        
        # For the dummy data, ensure prod_id is valid
        # In real data, prod_id should match the recipe's actual product
        if prod_id not in prod_ids and prod_ids:
            prod_id = random.choice(prod_ids)
        
        # Generate 5-10 parameters per recipe
        num_params = random.randint(5, 10)
        for j in range(num_params):
            param = generate_recipe_parameter(prod_id, recipe_id, j)
            all_parameters.append(param)
    
    return all_parameters


def generate_weekly_data(category_data, num_weeks=8):
    """
    Generates weekly data structure with nested dictionaries.
    
    Args:
        category_data (dict): Data containing category and prod_ids
        num_weeks (int): Number of weeks to generate data for
        
    Returns:
        dict: Weekly data with date keys and nested data
    """
    weekly_data = {}
    
    # Get devices information
    devices_info = get_r3_options()
    
    # Generate data for each week
    base_date = datetime.now() - timedelta(weeks=num_weeks)
    
    for week in range(num_weeks):
        # Calculate the Monday of each week
        week_date = base_date + timedelta(weeks=week)
        week_monday = week_date - timedelta(days=week_date.weekday())
        date_key = week_monday.strftime("%Y-%m-%d")
        
        # Generate data for this week
        rcp_info = generate_recipe_info_data(category_data["prod_ids"])
        # Extract recipe IDs for matching
        recipe_ids = rcp_info.get("all_recipe_ids", [])
        
        weekly_data[date_key] = {
            "rcp_info": rcp_info,
            "summary": generate_summary_data(category_data["prod_ids"]),
            "summary_by_category": generate_summary_data_by_category(category_data["prod_ids"]),
            "all_recipe_list": generate_all_recipe_list(category_data["prod_ids"], recipe_ids),
            "week_number": week + 1,
            "category": category_data["category"]
        }
    
    # Add devices info to the response
    return {
        "devices": devices_info["devices"],
        "weekly_data": weekly_data
    }


def get_all_data():
    """
    Returns all device statistics data with weekly structure.
    
    Returns:
        dict: All device statistics data organized by week
    """
    # Get all categories data
    options = get_r3_options()
    
    # Generate combined weekly data for all categories
    all_prod_ids = []
    for device in options["devices"]:
        all_prod_ids.extend(device["prod_ids"])
    
    combined_category = {
        "category": "ALL",
        "prod_ids": all_prod_ids
    }
    
    return generate_weekly_data(combined_category)


def get_working_devices_mapping():
    """
    Returns mapping of prod_id to prod_catg_cd2 (device category).
    
    Returns:
        dict: Dictionary with prod_id as keys and prod_catg_cd2 as values
    """
    options = get_r3_options()
    working_devices = {}
    
    # Map each prod_id to its category
    for device in options["devices"]:
        category = device["category"]
        for prod_id in device["prod_ids"]:
            working_devices[prod_id] = {
                "prod_id": prod_id,
                "prod_catg_cd2": category
            }
    
    return working_devices



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

    weekly_data = get_all_data()