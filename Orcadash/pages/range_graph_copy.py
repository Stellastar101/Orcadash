import OrcFxAPI
import taipy.gui.builder as tgb
from taipy.gui import State, Gui # Added State for type hinting callbacks, Gui for main
from taipy import Scenario, create_scenario # For type hinting scenario object
import pandas as pd
from datetime import datetime
import sys
import os
from typing import List, Dict, Tuple, Optional, Any # For type hinting
from taipy import Config, Scope, Orchestrator
from typing import List, Tuple, Union, Any, Optional # Added for type hinting
import plotly.graph_objects as go
from taipy import Config, Scope
import plotly.express as px
import plotly.graph_objects as go  # Ensure this is imported



# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from var_and_func.variables import variables_dict, file_paths


__all__ = [
    "file_paths", "file_lov", "default_file_path", 
    "lines", "lines_lov", "Selected_file", 
    "variable_category", "categories_lov", "variable", "variable_lov",
    "extracted_data", "extracted_columns", "extracted_data_str", 
    "data_available", "selected_statistic",
    "figure",
    "table_columns"  
]

# Initialize with default values
for var in __all__:
    if var not in globals():
        globals()[var] = None



PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#SITES_DATA_PATH: str = os.path.join(PROJECT_ROOT, 'data', 'site_data.csv')
#WEATHER_DATA_PATH: str = os.path.join(PROJECT_ROOT, 'data', 'weather_data.csv')
LOGO_PATH: str = os.path.join(PROJECT_ROOT, 'Orcadash.png')
# Initialize state variables
file_paths = []
file_lov = []
default_file_path = ["Select File"]

lines = []
lines_lov = []

Selected_file = ""

# Load variable categories from variables_dict
variable_category = list(variables_dict.keys())
categories_lov = variable_category

variable = ""
variable_lov = []

extracted_data = pd.DataFrame()
data_available = False
selected_statistic = "mean"


# Ensure all variables are properly initialized for Taipy state management
def initialize_state():
    return {
        "file_paths": [],
        "file_lov": [],
        "default_file_path": ["Select File"],
        "lines": [],
        "lines_lov": [],
        "Selected_file": "",
        "variable_category": list(variables_dict.keys()),
        "categories_lov": list(variables_dict.keys()),
        "variable": "",
        "variable_lov": [],
        "extracted_data": pd.DataFrame(),
        "extracted_data_str": "Select data and click 'Extract Data'",
        "extracted_columns": [], 
        "data_available": False,
        "selected_statistic": "mean",
        "figure": go.Figure(),
        "table_columns": [] 
    }


def on_file_selection(state, action, payload):
    """Handle file selection and update file_paths"""
    print(f"File selection callback - action: {action}, payload: {payload}")
    
    # Get the current file_paths from the file selector
    current_files = state.file_paths if hasattr(state, 'file_paths') else []
    
    # Always update file_lov to match file_paths
    if current_files:
        if isinstance(current_files, str):
            state.file_paths = [current_files]
            state.file_lov = [current_files]
        else:
            state.file_paths = list(current_files)
            state.file_lov = list(current_files)
    else:
        state.file_paths = []
        state.file_lov = []
    
    # Update selected file display
    if state.file_paths:
        state.Selected_file = state.file_paths[0]
    else:
        state.Selected_file = ""
    
    # Extract lines from the selected file
    if state.Selected_file:
        try:
            line_names = get_line_names(state.Selected_file)
            state.lines_lov = line_names
            state.lines = []  # Clear current selection
            print(f"Extracted {len(line_names)} lines from {state.Selected_file}")
        except Exception as e:
            print(f"Error extracting lines from {state.Selected_file}: {e}")
            state.lines_lov = []
    
    print(f"Current files: {current_files}")
    print(f"Updated file_paths: {state.file_paths}")
    print(f"Updated file_lov: {state.file_lov}")
    print(f"Updated lines_lov: {state.lines_lov}")
    print(f"Type of file_paths: {type(state.file_paths)}")
    print(f"Type of file_lov: {type(state.file_lov)}")

def on_file_change(state, var_name, var_val):
    """Handle file selection change from dropdown"""
    print(f"File change callback - var_name: {var_name}, var_val: {var_val}")
    
    if var_name == "file_paths" and var_val:
        # Ensure file_paths is a list
        if not hasattr(state, 'file_paths') or not isinstance(state.file_paths, list):
            state.file_paths = []
        
        state.Selected_file = var_val[0] if isinstance(var_val, list) else var_val
        print(f"Selected file changed to: {state.Selected_file}")
'''
def on_file_change(state, var_name, var_val):
    if var_name == "file_paths" and var_val:
        if not isinstance(state.file_paths, list):
            state.file_paths = []
        # Ensure var_val is always treated as a list
        if isinstance(var_val, str):  
            var_val = [var_val]
        # Append only unique files
        new_files = [file for file in var_val if file not in state.file_paths]
        if new_files:
            state.file_paths.extend(new_files)
            state.file_path_text = "File Paths Selected:\n" + "\n".join(state.file_paths)  # Update display
    print(f"Updated {var_name}: {var_val}")
'''
def change_category(state, var_name, var_val):
    """Handle category selection and update variables"""
    print(f"Category change callback - var_name: {var_name}, var_val: {var_val}")
    
    if var_name == "variable_category" and var_val:
        # Ensure variable_lov is a list
        if not hasattr(state, 'variable_lov') or not isinstance(state.variable_lov, list):
            state.variable_lov = []
        
        # Get the variables for the selected category
        category_variables = list(variables_dict[var_val].keys())
        state.variable_lov = category_variables
        state.variable = category_variables[0] if category_variables else ""
        print(f"Updated variables for category {var_val}: {category_variables}")

def update_file_lov(state, action, payload):
    """Manually update file_lov from file_paths"""
    print("Manual update of file_lov triggered")
    if hasattr(state, 'file_paths') and state.file_paths:
        if isinstance(state.file_paths, list):
            state.file_lov = state.file_paths.copy()
        else:
            state.file_lov = [state.file_paths]
        print(f"Updated file_lov: {state.file_lov}")
    else:
        state.file_lov = []
        print("Cleared file_lov")

def test_file_lov(state, action, payload):
    """Test function to manually set file_lov"""
    print("Test function triggered")
    test_files = ["test1.sim", "test2.sim", "test3.sim"]
    state.file_lov = test_files
    print(f"Set file_lov to: {state.file_lov}")

def get_line_names(file_path):
    """Load the OrcaFlex model and retrieve the names of all line objects."""
    try:
        # Load the OrcaFlex model by passing the file path to the Model constructor
        model = OrcFxAPI.Model(file_path)
        
        line_names = []
        for obj in model.objects:
            if obj.type == OrcFxAPI.otLine:
                line_names.append(obj.Name)
        
        print(f"Found {len(line_names)} lines in {file_path}")
        return line_names
    except Exception as e:
        print(f"Error loading model from {file_path}: {e}")
        return []

def extract_lines_from_file(state, action, payload):
    """Extract lines from the selected file and populate the line selector"""
    print("Extracting lines from selected file...")
    
    if hasattr(state, 'Selected_file') and state.Selected_file:
        try:
            # Get lines from the selected file
            line_names = get_line_names(state.Selected_file)
            
            # Update the lines_lov for the selector
            state.lines_lov = line_names
            state.lines = []  # Clear current selection
            
            print(f"Extracted {len(line_names)} lines: {line_names}")
            print(f"Updated lines_lov: {state.lines_lov}")
            
        except Exception as e:
            print(f"Error extracting lines: {e}")
            state.lines_lov = []
    else:
        print("No file selected for line extraction")
        state.lines_lov = []

def extract_range_graph_data(file_path, selected_line, selected_variable):
    """Extract range graph data for a specific line and variable"""
    try:
        model = OrcFxAPI.Model(file_path)
        line = model[selected_line]
        
        period = OrcFxAPI.PeriodNum.WholeSimulation
        #rg = line.RangeGraph(variable[selected_variable], period)
        rg = line.RangeGraph(selected_variable, period)
        
        df = pd.DataFrame({
            'z': rg.X,
            'min': rg.Min,
            'max': rg.Max,
            'mean': rg.Mean
        })
        
        print(f"Extracted {len(df)} data points for line '{selected_line}', variable '{selected_variable}'")
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame(columns=['z', 'min', 'max', 'mean'])

def extract_multiple_lines_data(file_path, selected_lines, selected_variable, selected_stat='mean'):
    """Extract data for multiple lines and combine into a single DataFrame"""
    try:
        combined_df = pd.DataFrame()
        
        for line in selected_lines:
            df = extract_range_graph_data(file_path, line, selected_variable)
            if not df.empty:
                # Create line-specific columns for the selected statistic
                line_df = pd.DataFrame({
                    'z': df['z'],
                    f"{line}_{selected_stat}": df[selected_stat]  # Use the selected statistic (min, max, mean)
                })
                
                if combined_df.empty:
                    combined_df = line_df
                else:
                    combined_df = pd.merge(combined_df, line_df, on='z', how='outer')
        
        print(f"Combined data for {len(selected_lines)} lines: {selected_lines}")
        return combined_df
    except Exception as e:
        print(f"Error comparing lines: {e}")
        return pd.DataFrame(columns=['z'])

def format_table_data(state):
    """Format data specifically for Taipy table display"""
    if hasattr(state, 'extracted_data') and not state.extracted_data.empty:
        # Create a clean copy
        df = state.extracted_data.copy()
        
        # Ensure proper column names (no special characters)
        df.columns = [str(col).replace(' ', '_').replace('-', '_') for col in df.columns]
        
        # Round numeric columns to reasonable precision
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df[col] = df[col].round(6)
        
        # Ensure proper index
        df = df.reset_index(drop=True)
        
        return df
    return pd.DataFrame()


def get_table_columns(state):
    """Get properly formatted column list for table display"""
    if hasattr(state, 'extracted_data') and not state.extracted_data.empty:
        return list(state.extracted_data.columns)
    return []
'''
def create_range_graph_figure(df, statistic):
    """Create Plotly figure for range graph data"""
    if df.empty or len(df.columns) < 2:
        return go.Figure()
    
    fig = go.Figure()
    z = df['z']
    
    # Add each line's data to the figure
    for col in df.columns[1:]:
        if col != 'z':
            line_name = col.replace(f'_{statistic}', '')
            fig.add_trace(go.Scatter(
                x=df[col],
                y=z,
                name=line_name,
                mode='lines'
            ))
    
    # Customize layout
    fig.update_layout(
        title=f"{df.columns[1].split('_')[0]} Comparison",
        xaxis_title=df.columns[1].split('_')[-1],
        yaxis_title="Depth (m)",
        legend_title="Lines",
        hovermode="y unified"
    )
    return fig
'''
def extract_range_graph_data(file_path, selected_line, selected_variable):
    """Extract range graph data for a specific line and variable"""
    try:
        model = OrcFxAPI.Model(file_path)
        line = model[selected_line]
        
        period = OrcFxAPI.PeriodNum.WholeSimulation
        #rg = line.RangeGraph(variable[selected_variable], period)
        rg = line.RangeGraph(selected_variable, period)
        
        df = pd.DataFrame({
            'z': rg.X,
            'min': rg.Min,
            'max': rg.Max,
            'mean': rg.Mean
        })
        
        print(f"Extracted {len(df)} data points for line '{selected_line}', variable '{selected_variable}'")
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame(columns=['z', 'min', 'max', 'mean'])

    '''
    fig.update_layout(
        title=f"{state.variable} Comparison",
        xaxis_title="Depth (m)",
        yaxis_title=f"{state.variable} ({statistic.capitalize()})",
        legend_title="Lines",
        hovermode="x unified",
        height=600
    )
    '''
def create_range_graph_figure(df, statistic):
    """Create Plotly figure with depth on X-axis and values on Y-axis"""
    if df.empty or len(df.columns) < 2:
        return go.Figure()
    
    fig = go.Figure()
    
    # Add each line's data to the figure
    for col in df.columns:
        if col != 'z' and col.endswith(statistic):
            line_name = col.replace(f'_{statistic}', '')
            fig.add_trace(go.Scatter(
                x=df['z'],  # Depth on X-axis
                y=df[col],  # Value on Y-axis
                name=line_name,
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=5)
            ))
    
    # Customize layout with depth on X-axis
    fig.update_layout(
        title=f"{df.columns[1].split('_')[0]} Comparison",
        xaxis_title="Arc (m)",
        yaxis_title=df.columns[1].split('_')[-1],
        legend_title="Lines",
        hovermode="x unified",
        height=600
    )
   
    # Add grid and better axis formatting
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    
    return fig

# Update the extract_range_graph_data function to ensure z is extracted as depth
# Update the process_selected_data function to include extracted_columns
def process_selected_data(state, action, payload):
    """Process the selected file, lines, and variable to extract data"""
    print("Processing selected data...")
    
    # Clear previous data immediately
    state.extracted_data = pd.DataFrame()
    state.data_available = False
    state.extracted_data_str = "Processing data..."
    state.extracted_columns = []  # Add this line
    
    if not state.Selected_file:
        print("No file selected")
        state.extracted_data_str = "Error: No file selected"
        return
    
    if not state.lines:
        print("No lines selected")
        state.extracted_data_str = "Error: No lines selected"
        return
    
    if not state.variable:
        print("No variable selected")
        state.extracted_data_str = "Error: No variable selected"
        return
    
    try:
        # Extract data for selected lines and variable
        selected_lines = state.lines if isinstance(state.lines, list) else [state.lines]
        selected_variable = state.variable
        
        print(f"Processing: File={state.Selected_file}, Lines={selected_lines}, Variable={selected_variable}")
        
        # Extract the data
        result_df = extract_multiple_lines_data(
            state.Selected_file, 
            selected_lines, 
            selected_variable,
            state.selected_statistic
        )
        

        
        if not result_df.empty:
            # Convert columns to string and reset index
            result_df.columns = result_df.columns.astype(str)
            result_df = result_df.reset_index(drop=True)

            # Convert to numeric where possible
            for col in result_df.columns:
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce')

            # Create visualization figure
            state.figure = create_range_graph_figure(result_df, state.selected_statistic)

            # Store data
            state.extracted_data = result_df
            print(f"State extracted data: {state.extracted_data}")
            state.extracted_columns = list(result_df.columns)
            state.data_available = True
            state.figure = create_range_graph_figure(result_df, state.selected_statistic)
            state.table_columns = [{"name": col, "id": col} for col in result_df.columns]          
            # Create a simplified string representation
            state.extracted_data_str = "Extracted Data:\n\n"
            state.extracted_data_str += f"Shape: {result_df.shape[0]} rows, {result_df.shape[1]} columns\n"
            state.extracted_data_str += f"Columns: {', '.join(result_df.columns)}\n\n"
            state.extracted_data_str += "First 10 rows:\n"
            state.extracted_data_str += result_df.head(10).to_string(index=False)
            
            state.data_available = True
            
            print(f"Successfully processed data with {len(result_df)} rows")
            print(f"Columns: {list(result_df.columns)}")
            
        else:
            state.extracted_data = pd.DataFrame()
            state.extracted_data_str = "No data extracted (empty result)"
            state.extracted_columns = []  # Add this line
            state.data_available = False
            print("No data extracted")
            
    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()
        
        state.extracted_data = pd.DataFrame()
        state.extracted_data_str = f"Error: {str(e)}"
        state.extracted_columns = []  # Add this line
        state.data_available = False

def ensure_data_format(state):
    """Ensure extracted_data is properly formatted for Taipy display"""
    if hasattr(state, 'extracted_data') and not state.extracted_data.empty:
        # Ensure all columns are strings
        state.extracted_data.columns = state.extracted_data.columns.astype(str)
        
        # Ensure index is reset
        state.extracted_data = state.extracted_data.reset_index(drop=True)
        
        # Ensure all data is numeric or string (no mixed types)
        for col in state.extracted_data.columns:
            if state.extracted_data[col].dtype == 'object':
                state.extracted_data[col] = state.extracted_data[col].astype(str)
        
        print(f"Data formatting check - Shape: {state.extracted_data.shape}")
        print(f"Columns: {list(state.extracted_data.columns)}")
        print(f"Data types: {state.extracted_data.dtypes.to_dict()}")
def export_to_csv(state):
    """Export extracted data to CSV file"""
    if not state.extracted_data.empty:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"extracted_data_{timestamp}.csv"
            state.extracted_data.to_csv(filename, index=False)
            state.extracted_data_str += f"\n\nData exported to: {os.path.abspath(filename)}"
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Export error: {e}")
            state.extracted_data_str += f"\n\nExport error: {str(e)}"
############################### GUI #########################################################


with tgb.Page() as page:    
    with tgb.part(class_name="card"):
        tgb.text("# Post Sim result dashboard", mode="md", class_name="text-center mt-1")
        with tgb.layout("40 20 40 ", class_name= "mb-1",gap="20px"): 
            tgb.text("")
            tgb.image(
                content=LOGO_PATH,       # Assuming LOGO_PATH is a variable containing a path or URL
                mode="md",
                class_name="text-center",
                width="100%",
                height="100%"
        )
    tgb.html("br")

    with tgb.part(class_name="card"):
        with tgb.layout(columns="1 2 2 ", gap="5px"):
            with tgb.part():
                tgb.text("Select .sim file **From**", mode="md")
                tgb.file_selector(
                    label="Select File to process",
                    content="{file_paths}",
                    multiple=True,
                    extensions=".sim,.Sim",
                )
                tgb.button(
                    "Process Selected Files",
                    on_action=on_file_selection,
                    class_name="plain"
                )
            with tgb.part():
                tgb.text("Select **FILES**", mode="md")
                tgb.selector(
                    value="{file_paths}",
                    lov="{file_lov}",
                    multiple=True,
                    on_change=on_file_change,
                    dropdown=True,
                )
                tgb.button(
                     "Extract Lines",
                     on_action=extract_lines_from_file,
                     class_name="plain"
                 )
            with tgb.part():
                tgb.text("Select **Line/s**", mode="md")
                tgb.selector(
                    value="{lines}",
                    lov="{lines_lov}",
                    multiple=True,
                    #on_change=change_category,
                    dropdown=True,
                )
            

    #tgb.html("br")
    with tgb.part(class_name="card"):
        with tgb.layout(columns="1 2 2 "):
            with tgb.part():
                tgb.text("Select **.sim** file ", mode="md")
                tgb.text(
                    "Selected file is: {Selected_file}",
                    mode="md",
                )
            with tgb.part():
                tgb.text("Select **Results Category**", mode="md")
                tgb.selector(
                    value="{variable_category}",
                    lov="{categories_lov}",
                    on_change=change_category,
                    dropdown=True,
                )
                tgb.text("Select results **variable**", mode="md")
                tgb.selector(
                    value="{variable}",
                    lov="{variable_lov}",
                    dropdown=True,
                )
                tgb.text("Select **statistic**", mode="md")
                tgb.selector(
                    value="{selected_statistic}",
                    lov=["min", "max", "mean"],
                    dropdown=True,
                    multiple=False,
                )
                tgb.button(
                    "Extract Data",
                    on_action=process_selected_data,
                    class_name="plain"
                )
            with tgb.part():
                 tgb.text("**Debug Info**", mode="md")
                 tgb.text(
                     "File paths: {file_paths}",
                     mode="md",
                 )
                 tgb.text(
                     "File lov: {file_lov}",
                     mode="md",
                 )
                 tgb.text(
                     "Lines lov: {lines_lov}",
                     mode="md",
                 )
                 tgb.button(
                     "Update File List",
                     on_action=update_file_lov,
                     class_name="plain"
                 )
                 tgb.button(
                     "Test File List",
                     on_action=test_file_lov,
                     class_name="plain"
                 )
                 tgb.button(
                     "Extract Lines",
                     on_action=extract_lines_from_file,
                     class_name="plain"
                 )

    # Data display section
    

# Al    so, let's add a function to ensure proper data formatting
            # Temporary debug section (add this before the table)
    tgb.text("Debug - Data type: {type(extracted_data)}", mode="md")
    tgb.text("Debug - Data empty: {extracted_data.empty}", mode="md") 
    tgb.text("Debug - Data available: {data_available}", mode="md")
    tgb.html("br")
    with tgb.part(class_name="card"):
        with tgb.part(render="{data_available}"):
            tgb.text("**Data Visualization**", mode="md")
            tgb.chart(
                figure="{figure}",
                style="height: 500px; width: 100%;"
            )
    tgb.html("br")
    with tgb.part(class_name="card"):
        tgb.text("**Data Visualization**", mode="md")
        tgb.table(
            data="{extracted_data}",
            columns="{table_columns}",
            editable=False,
            width="100%",
            height="400px",
            page_size=20
        )
    with tgb.part(class_name="card"):
        tgb.text("**Extracted Data**", mode="md")
        
        # Status information
        tgb.text("Data available: {data_available}", mode="md")
        tgb.text("Selected file: {Selected_file}", mode="md")
        tgb.text("Selected lines: {lines}", mode="md")
        tgb.text("Selected variable: {variable}", mode="md")
        tgb.text("Selected statistic: {selected_statistic}", mode="md")
        
        # Show data info when available
        with tgb.part(render="{data_available}"):
            tgb.text("Data shape: {len(extracted_data)} rows, {len(extracted_data.columns)} columns", mode="md")
            tgb.text("Columns: {list(extracted_data.columns)}", mode="md")
            
            # Main data table - SINGLE TABLE DEFINITION
            tgb.table(
                data="{extracted_data}",
                editable=False,
                width="100%",
                height="400px",
                page_size=20
            )
            
            # Data visualization
            with tgb.part():
                tgb.text("**Data Visualization**", mode="md")
                with tgb.part(render="{len(extracted_data.columns) > 1}"):
                    tgb.chart(
                        data="{extracted_data}",
                        x="z",
                        y="{list(extracted_data.columns)[1] if len(extracted_data.columns) > 1 else ''}",
                        type="line"
                    )
        
        # Show text version when table might have issues
        with tgb.part():
            tgb.text("**Text Preview**", mode="md")
            tgb.text("{extracted_data_str}", mode="pre")
        
        # Export functionality
        with tgb.part(render="{data_available}"):
            tgb.button(
                "Export to CSV",
                on_action=lambda state, _, __: export_to_csv(state),
                class_name="plain"
            )
    with tgb.part(class_name="card"):
        with tgb.part(render="{data_available}"):
            tgb.text("Data shape: {len(extracted_data)} rows, {len(extracted_data.columns)} columns", mode="md")
            tgb.text("Columns: {', '.join(extracted_columns)}", mode="md")
            
            # Simplified table columns definition
            tgb.table(
                data="{extracted_data}",
                columns="{table_columns}",
                editable=False,
                width="100%",
                height="400px",
                page_size=20
            )
            
            # Enhanced chart section
            tgb.text("**Data Visualization**", mode="md")
            tgb.chart(
                figure="{figure}",
                style="height: 500px; width: 100%;"
            )
    

# Also, let's add a function to ensure proper data formatting
# ------------------------------------------
# Make the state variables visible globally
# so Taipy can find them at page-parse time
initial_state = initialize_state()
extracted_data  = initial_state["extracted_data"]
data_available  = initial_state["data_available"]
selected_statistic = initial_state["selected_statistic"]
# … add any other keys you reference in the page
# ------------------------------------------
     
if __name__ == "__main__":
    # Initialize state variables
    initial_state = initialize_state()
    
    # Declare all state variables in global scope
    for var_name, value in initial_state.items():
        globals()[var_name] = value
    
    Gui(page=page).run(
        title="Orcaflex results generator", 
        dark_mode=False, 
        debug=True, 
        use_reloader=True, 
        margin="5em",
        state=initial_state,
        port="auto"
    )
