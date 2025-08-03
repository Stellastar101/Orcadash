Range_Graph_variable_dict = {
    "Position": ["X", "Y", "Z", "Expansion Factor"],
    "Motions": ["Velocity", "GX-Velocity", "GY-Velocity", "GZ-Velocity", "Acceleration", "GX-Acceleration", "GY-Acceleration", "GZ-Acceleration", "Acceleration rel. g", "x-Acceleration rel. g", "y-Acceleration rel. g", "z-Acceleration rel. g"],
    "Angles": ["Azimuth", "Declination", "Gamma", "Twist", "Fluid Incidence Angle", "Ez-Angle", "Exy-Angle", "Ezx-Angle", "Ezy-Angle"],
    "Forces": ["Effective Tension", "Normalised Tension", "Contents Density", "Shear Force", "x-Shear Force", "y-Shear Force", "Shear Force component", "In-plane Shear Force", "Out-of-plane Shear Force"],
    "Moments": ["Bend Moment", "x-Bend Moment", "y-Bend Moment", "Bend Moment component", "In-plane Bend Moment", "Out-of-plane Bend Moment", "Curvature", "Normalised Curvature", "x-Curvature", "y-Curvature", "Curvature component", "In-plane Curvature", "Out-of-plane Curvature", "Bend Radius", "x-Bend Radius", "y-Bend Radius", "Bend Radius component", "In-plane Bend Radius", "Out-of-plane Bend Radius"],
    "Contact": ["Line Clearance", "Line Centreline Clearance", "Seabed Clearance", "Vertical Seabed Clearance", "Line Clash Force", "Line Clash Energy", "Solid Contact Force", "Seabed Normal Penetration/D", "Seabed Normal Resistance", "Seabed Normal Resistance/D"],
    "Pipe Stress/Strain": ["Direct Tensile Strain", "Max Bending Strain", "Worst ZZ Strain", "ZZ Strain", "Max von Mises Stress", "Max Bending Stress", "Worst ZZ Stress", "Direct Tensile Stress", "Worst Hoop Stress", "Max xy-Shear Stress", "Internal Pressure", "External Pressure", "Net Internal Pressure", "von Mises Stress", "RR Stress", "CC Stress", "ZZ Stress", "RC Stress", "RZ Stress", "CZ Stress"],
    "Code Checks": ["API RP 2RD Stress", "API RP 2RD Utilisation", "API RP 1111 LLD", "API RP 1111 CLD", "API RP 1111 BEP", "API RP 1111 Max Combined", "DNV OS F101 Disp. Controlled", "DNV OS F101 Load Controlled", "DNV OS F101 Simplified Strain", "DNV OS F101 Simplified Stress", "DNV OS F101 Tension Utilisation", "DNV OS F201 LRFD", "DNV OS F201 WSD", "PD 8010 Allowable Stress Check", "PD 8010 Axial Compression Check", "PD 8010 Bending Check", "PD 8010 Torsion Check", "PD 8010 Load Combinations Check", "PD 8010 Bending Strain Check"],
    "Fluid Loads": ["Relative Velocity", "Normal Relative Velocity", "Axial Relative Velocity", "Strouhal Frequency", "Reynolds number", "x-Drag Coefficient", "y-Drag Coefficient", "z-Drag Coefficient", "Lift Coefficient", "Sea Surface Z", "Depth", "Sea Surface Clearance", "Proportion Wet"]
}
#category_lov= ["Position", "Motions", "Angles", "Forces", "Moments", "Contact]
category_lov= list(Range_Graph_variable_dict.keys())
#print(category_lov)

variables_dict = {
    "Position": {
        "X": "m",
        "Y": "m", 
        "Z": "m",
        "Expansion Factor": "-"
    },
    "Motions": {
        "Velocity": "m/s",
        "GX-Velocity": "m/s",
        "GY-Velocity": "m/s", 
        "GZ-Velocity": "m/s",
        "Acceleration": "m/s²",
        "GX-Acceleration": "m/s²",
        "GY-Acceleration": "m/s²",
        "GZ-Acceleration": "m/s²",
        "Acceleration rel. g": "g",
        "x-Acceleration rel. g": "g",
        "y-Acceleration rel. g": "g",
        "z-Acceleration rel. g": "g"
    },
    "Angles": {
        "Azimuth": "°",
        "Declination": "°",
        "Gamma": "°",
        "Twist": "°",
        "Fluid Incidence Angle": "°",
        "Ez-Angle": "°",
        "Exy-Angle": "°",
        "Ezx-Angle": "°",
        "Ezy-Angle": "°"
    },
    "Forces": {
        "Effective Tension": "N",
        "Normalised Tension": "-",
        "Contents Density": "kg/m³",
        "Shear Force": "N",
        "x-Shear Force": "N",
        "y-Shear Force": "N",
        "Shear Force component": "N",
        "In-plane Shear Force": "N",
        "Out-of-plane Shear Force": "N"
    },
    "Moments": {
        "Bend Moment": "N·m",
        "x-Bend Moment": "N·m",
        "y-Bend Moment": "N·m",
        "Bend Moment component": "N·m",
        "In-plane Bend Moment": "N·m",
        "Out-of-plane Bend Moment": "N·m",
        "Curvature": "1/m",
        "Normalised Curvature": "-",
        "x-Curvature": "1/m",
        "y-Curvature": "1/m",
        "Curvature component": "1/m",
        "In-plane Curvature": "1/m",
        "Out-of-plane Curvature": "1/m",
        "Bend Radius": "m",
        "x-Bend Radius": "m",
        "y-Bend Radius": "m",
        "Bend Radius component": "m",
        "In-plane Bend Radius": "m",
        "Out-of-plane Bend Radius": "m"
    },
    "Contact": {
        "Line Clearance": "m",
        "Line Centreline Clearance": "m",
        "Seabed Clearance": "m",
        "Vertical Seabed Clearance": "m",
        "Line Clash Force": "N",
        "Line Clash Energy": "J",
        "Solid Contact Force": "N",
        "Seabed Normal Penetration/D": "-",
        "Seabed Normal Resistance": "N",
        "Seabed Normal Resistance/D": "N/m"
    },
    "Pipe Stress/Strain": {
        "Direct Tensile Strain": "-",
        "Max Bending Strain": "-",
        "Worst ZZ Strain": "-",
        "ZZ Strain": "-",
        "Max von Mises Stress": "Pa",
        "Max Bending Stress": "Pa",
        "Worst ZZ Stress": "Pa",
        "Direct Tensile Stress": "Pa",
        "Worst Hoop Stress": "Pa",
        "Max xy-Shear Stress": "Pa",
        "Internal Pressure": "Pa",
        "External Pressure": "Pa",
        "Net Internal Pressure": "Pa",
        "von Mises Stress": "Pa",
        "RR Stress": "Pa",
        "CC Stress": "Pa",
        "ZZ Stress": "Pa",
        "RC Stress": "Pa",
        "RZ Stress": "Pa",
        "CZ Stress": "Pa"
    },
    "Code Checks": {
        "API RP 2RD Stress": "Pa",
        "API RP 2RD Utilisation": "-",
        "API RP 1111 LLD": "-",
        "API RP 1111 CLD": "-",
        "API RP 1111 BEP": "-",
        "API RP 1111 Max Combined": "-",
        "DNV OS F101 Disp. Controlled": "-",
        "DNV OS F101 Load Controlled": "-",
        "DNV OS F101 Simplified Strain": "-",
        "DNV OS F101 Simplified Stress": "Pa",
        "DNV OS F101 Tension Utilisation": "-",
        "DNV OS F201 LRFD": "-",
        "DNV OS F201 WSD": "-",
        "PD 8010 Allowable Stress Check": "-",
        "PD 8010 Axial Compression Check": "-",
        "PD 8010 Bending Check": "-",
        "PD 8010 Torsion Check": "-",
        "PD 8010 Load Combinations Check": "-",
        "PD 8010 Bending Strain Check": "-"
    },
    "Fluid Loads": {
        "Relative Velocity": "m/s",
        "Normal Relative Velocity": "m/s",
        "Axial Relative Velocity": "m/s",
        "Strouhal Frequency": "Hz",
        "Reynolds number": "-",
        "x-Drag Coefficient": "-",
        "y-Drag Coefficient": "-",
        "z-Drag Coefficient": "-",
        "Lift Coefficient": "-",
        "Sea Surface Z": "m",
        "Depth": "m",
        "Sea Surface Clearance": "m",
        "Proportion Wet": "-"
    }
}
#variable_category = (list(variables_dict.keys()))
def generate_variable(selected_variable):
    """
    Generate variables for a specific category from variables_dict.
    
    Args:
        selected_variable (str): The category key from variables_dict
        
    Returns:
        dict: Dictionary containing variable names and their units for the selected category
    """
    if selected_variable in variables_dict:
        return variables_dict[selected_variable]
    else:
        return {}

def generate_variables_from_keys(keys_list):
    """
    Generate values from variables_dict when passing a list of keys.
    
    Args:
        keys_list (list): List of category keys from variables_dict
        
    Returns:
        dict: Combined dictionary containing all variables and their units for the specified categories
    """
    result = {}
    
    for key in keys_list:
        if key in variables_dict:
            result.update(variables_dict[key])
        else:
            print(f"Warning: Key '{key}' not found in variables_dict")
    
    return result

def get_all_variables():
    """
    Get all variables from variables_dict.
    
    Returns:
        dict: Complete variables_dict
    """
    return variables_dict

def get_variable_units(variable_name):
    """
    Get the units for a specific variable.
    
    Args:
        variable_name (str): Name of the variable
        
    Returns:
        str: Units for the variable, or None if not found
    """
    for category, variables in variables_dict.items():
        if variable_name in variables:
            return variables[variable_name]
    return None

# Example usage and testing
if __name__ == "__main__":
    # Test the new function
    selected_categories = ["Forces", "Moments"]
    result = generate_variables_from_keys(selected_categories)
    print("Generated variables for Forces and Moments:")
    print(result)
    
    # Test getting all variables
    all_vars = get_all_variables()
    print(f"\nTotal categories: {len(all_vars)}")
    
    # Test getting units for a specific variable
    units = get_variable_units("Effective Tension")
    print(f"\nUnits for 'Effective Tension': {units}")