import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_wafer_mp_info(num_records=50):
    """Generate dummy wafer measurement point information"""
    data = []
    
    for i in range(num_records):
        chip_x = random.randint(1, 10)
        chip_y = random.randint(1, 10)
        
        record = {
            "ChipNo_X": chip_x,
            "ChipNo_Y": chip_y,
            "Coordinate_X": round(random.uniform(-50.0, 50.0), 3),
            "Coordinate_Y": round(random.uniform(-50.0, 50.0), 3),
            "P_No": random.randint(1, 20),
            "D_No": random.randint(1, 100),
            "Diff": random.choice([True, False]),
            "Rel": random.choice([True, False]),
            "Rel_MoveX": round(random.uniform(-5.0, 5.0), 3),
            "RelMoveY": round(random.uniform(-5.0, 5.0), 3),
            "Coordinate_X_r": round(random.uniform(-50.0, 50.0), 3),
            "Coordinate_Y_r": round(random.uniform(-50.0, 50.0), 3),
            "Parameter": f"Para_{random.randint(1, 20)}",
            "img_meas2": f"IMG_MEAS_{i+1:04d}.jpg"
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_wafer_align_info(num_records=10):
    """Generate dummy wafer alignment information"""
    data = []
    
    for i in range(num_records):
        record = {
            "Align_No": i + 1,
            "Chip.X": random.randint(1, 10),
            "Chip.Y": random.randint(1, 10),
            "Coordinate.X": round(random.uniform(-100.0, 100.0), 3),
            "Coordinate.Y": round(random.uniform(-100.0, 100.0), 3),
            "P.No": random.randint(1, 20)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_idp_image_info(num_records=20):
    """Generate dummy IDP image information"""
    data = []
    
    for i in range(num_records):
        p_no = random.randint(1, 20)
        seq = i + 1
        
        record = {
            "Parameter": f"Para_{p_no}",
            "img_add1": f"IMG_ADD1_{seq:04d}.jpg",
            "img_add2": f"IMG_ADD2_{seq:04d}.jpg",
            "img_meas1": f"IMG_MEAS1_{seq:04d}.jpg",
            "img_meas2": f"IMG_MEAS2_{seq:04d}.jpg",
            "SEQ": seq,
            "Last_SEQ": seq + random.randint(0, 5),
            "Region": p_no,  # Region is the same as P_No
            "image_add3": f"IMG_ADD3_{seq:04d}.jpg",
            "Addressing": random.choice(["Yes", "No"]),
            "Mother_Para": f"Para_{random.randint(1, 5)}",
            "Double_Addressing": random.choice([True, False]),
            "Meas_Counting": random.randint(1, 10),
            "dnumber_removed": random.randint(0, 3)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def get_recipe_open_data(recipe_id=None, fac_id=None, tool_category=None):
    """
    Generate and return all three dataframes as dictionaries for a recipe
    """
    # Generate the dataframes
    wafer_mp_df = generate_wafer_mp_info()
    wafer_align_df = generate_wafer_align_info()
    idp_image_df = generate_idp_image_info()
    
    # Convert to dictionaries using records orientation
    result = {
        "wafer_mp_info": wafer_mp_df.to_dict("records"),
        "wafer_align_info": wafer_align_df.to_dict("records"),
        "idp_image_info": idp_image_df.to_dict("records"),
        "recipe_id": recipe_id or "DUMMY_RECIPE_001",
        "fac_id": fac_id or "R3",
        "tool_category": tool_category or "cd-sem",
        "timestamp": datetime.now().isoformat()
    }
    
    return result

# Export the dataframes if needed for direct access
wafer_mp_df = generate_wafer_mp_info()
wafer_align_df = generate_wafer_align_info()
idp_image_df = generate_idp_image_info()