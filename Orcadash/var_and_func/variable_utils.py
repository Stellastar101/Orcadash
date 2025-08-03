"""
Utility functions for working with variables_dict.
This module provides functions to generate and manipulate variable data from the variables_dict.
"""

from .variables import variables_dict, generate_variables_from_keys, generate_variable, get_all_variables, get_variable_units

def generate_variables_by_category(category_list):
    """
    Generate variables for specific categories.
    
    Args:
        category_list (list): List of category names to extract variables from
        
    Returns:
        dict: Dictionary with category names as keys and their variables as values
    """
    result = {}
    for category in category_list:
        if category in variables_dict:
            result[category] = variables_dict[category]
        else:
            print(f"Warning: Category '{category}' not found")
    return result

def get_variables_with_units(category_list):
    """
    Get variables with their units for specified categories.
    
    Args:
        category_list (list): List of category names
        
    Returns:
        dict: Flat dictionary with variable names as keys and units as values
    """
    return generate_variables_from_keys(category_list)

def filter_variables_by_unit(unit_filter, category_list=None):
    """
    Filter variables by their units.
    
    Args:
        unit_filter (str): Unit to filter by (e.g., "N", "m/s", "Pa")
        category_list (list, optional): List of categories to search in. If None, searches all categories.
        
    Returns:
        dict: Dictionary containing variables that match the unit filter
    """
    result = {}
    
    if category_list is None:
        categories_to_search = variables_dict.keys()
    else:
        categories_to_search = [cat for cat in category_list if cat in variables_dict]
    
    for category in categories_to_search:
        for variable, unit in variables_dict[category].items():
            if unit == unit_filter:
                result[variable] = unit
    
    return result

def get_variable_categories():
    """
    Get all available category names.
    
    Returns:
        list: List of all category names in variables_dict
    """
    return list(variables_dict.keys())

def search_variables(search_term, category_list=None):
    """
    Search for variables containing a specific term.
    
    Args:
        search_term (str): Term to search for in variable names
        category_list (list, optional): List of categories to search in. If None, searches all categories.
        
    Returns:
        dict: Dictionary containing matching variables and their units
    """
    result = {}
    
    if category_list is None:
        categories_to_search = variables_dict.keys()
    else:
        categories_to_search = [cat for cat in category_list if cat in variables_dict]
    
    for category in categories_to_search:
        for variable, unit in variables_dict[category].items():
            if search_term.lower() in variable.lower():
                result[variable] = unit
    
    return result

# Example usage functions
def example_usage():
    """
    Demonstrate various ways to use the variable generation functions.
    """
    print("=== Variable Generation Examples ===\n")
    
    # Example 1: Generate variables for specific categories
    print("1. Generating variables for 'Forces' and 'Moments':")
    forces_moments = generate_variables_from_keys(["Forces", "Moments"])
    for var, unit in forces_moments.items():
        print(f"   {var}: {unit}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Get all categories
    print("2. All available categories:")
    categories = get_variable_categories()
    for i, cat in enumerate(categories, 1):
        print(f"   {i}. {cat}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Filter by unit
    print("3. All variables with units 'N' (Newtons):")
    newton_vars = filter_variables_by_unit("N")
    for var, unit in newton_vars.items():
        print(f"   {var}: {unit}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Search for variables containing "Tension"
    print("4. Variables containing 'Tension':")
    tension_vars = search_variables("Tension")
    for var, unit in tension_vars.items():
        print(f"   {var}: {unit}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Get units for specific variable
    print("5. Units for specific variables:")
    test_vars = ["Effective Tension", "Velocity", "Azimuth"]
    for var in test_vars:
        units = get_variable_units(var)
        print(f"   {var}: {units}")

if __name__ == "__main__":
    example_usage() 