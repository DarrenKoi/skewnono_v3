import random
from datetime import datetime

def generate_recipe_list(fac_id=None, tool_category=None):
    """
    Generate dummy recipe list based on facility and tool category
    """
    # Base recipe names
    base_recipes = [
        "RECIPE_STANDARD",
        "RECIPE_ADVANCED", 
        "RECIPE_CUSTOM",
        "RECIPE_TEST",
        "RECIPE_PRODUCTION",
        "RECIPE_SPECIAL",
        "RECIPE_MAINTENANCE",
        "RECIPE_CALIBRATION",
        "RECIPE_VALIDATION",
        "RECIPE_EMERGENCY",
        "RECIPE_BASELINE",
        "RECIPE_ENHANCED",
        "RECIPE_OPTIMIZED",
        "RECIPE_EXPERIMENTAL",
        "RECIPE_BACKUP"
    ]
    
    # Facility-specific prefixes
    fac_prefixes = {
        'R3': 'R3',
        'R2': 'R2', 
        'R1': 'R1',
        'F12': 'F12',
        'F13': 'F13'
    }
    
    # Tool-specific suffixes
    tool_suffixes = {
        'cd-sem': ['CD', 'SEM', 'MEAS'],
        'hv-sem': ['HV', 'HIGH', 'VOLT'],
        'verity': ['VER', 'VERITY', 'CHECK'],
        'provision': ['PROV', 'PROVISION', 'SETUP']
    }
    
    # Generate recipe list
    recipes = []
    fac_prefix = fac_prefixes.get(fac_id, fac_id or 'R3')
    tool_suffix_list = tool_suffixes.get(tool_category, ['GENERIC'])
    
    # Generate 15-25 recipes per tool/facility combination
    num_recipes = random.randint(15, 25)
    selected_bases = random.sample(base_recipes, min(num_recipes, len(base_recipes)))
    
    for i, base_name in enumerate(selected_bases):
        # Add some variety with different versions and suffixes
        version = random.randint(1, 9)
        suffix = random.choice(tool_suffix_list)
        
        # Create recipe name: FAC_BASENAME_VERSION_TOOLSUFFIX
        recipe_name = f"{fac_prefix}_{base_name}_{version:02d}_{suffix}"
        
        # Add some recipes without tool suffix for variety
        if random.random() < 0.3:  # 30% chance
            recipe_name = f"{fac_prefix}_{base_name}_{version:02d}"
            
        recipes.append(recipe_name)
    
    # Add some additional random recipes with different patterns
    additional_patterns = [
        f"{fac_prefix}_DAILY_{random.randint(1, 31):02d}_{random.choice(tool_suffix_list)}",
        f"{fac_prefix}_WEEKLY_{random.randint(1, 52):02d}",
        f"{fac_prefix}_MONTHLY_{random.randint(1, 12):02d}_{random.choice(tool_suffix_list)}",
        f"{fac_prefix}_SHIFT_{random.choice(['A', 'B', 'C'])}_{random.choice(tool_suffix_list)}"
    ]
    
    # Add 2-4 additional recipes
    recipes.extend(random.sample(additional_patterns, random.randint(2, 4)))
    
    # Sort recipes for consistent ordering
    recipes.sort()
    
    return recipes

def get_recipe_list_response(fac_id=None, tool_category=None):
    """
    Generate response data for recipe list API
    """
    recipe_list = generate_recipe_list(fac_id, tool_category)
    
    return {
        "recipe_list": recipe_list,
        "fac_id": fac_id or "R3",
        "tool_category": tool_category or "cd-sem",
        "total_count": len(recipe_list),
        "timestamp": datetime.now().isoformat()
    }

# Export default data for direct access
recipe_list = generate_recipe_list()
data = get_recipe_list_response()