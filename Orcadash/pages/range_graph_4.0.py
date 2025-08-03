# pages/range_graph.py
from taipy.gui import Gui, notify
#from taipy.gui.page import page
from taipy.gui.builder import page
from taipy.gui.controls import *
import pandas as pd
import OrcFxAPI
from datetime import datetime
import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(PROJECT_ROOT, 'Orcadash.png')
# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from var_and_func.variables import variables_dict, file_paths
# Initialize state
file_paths = []
file_lov = []
default_file_path = ["Select File"]
Selected_file = ""
lines = []
lines_lov = []
variable_category = list(variables_dict.keys())
categories_lov = variable_category
variable = ""
variable_lov = []
extracted_data = pd.DataFrame()
data_available = False
selected_statistic = "mean"

# ========== Logic Functions (unchanged) ==========

def get_line_names(file_path):
    try:
        model = OrcFxAPI.Model(file_path)
        return [obj.Name for obj in model.objects if obj.type == OrcFxAPI.otLine]
    except Exception as e:
        print(f"Error reading OrcaFlex model: {e}")
        return []

def extract_range_graph_data(file_path, selected_line, selected_variable):
    try:
        model = OrcFxAPI.Model(file_path)
        line = model[selected_line]
        period = OrcFxAPI.PeriodNum.WholeSimulation
        rg = line.RangeGraph(selected_variable, period)
        return pd.DataFrame({
            'z': rg.X,
            'min': rg.Min,
            'max': rg.Max,
            'mean': rg.Mean
        })
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()

def extract_multiple_lines_data(file_path, selected_lines, selected_variable, selected_stat='mean'):
    try:
        combined_df = pd.DataFrame()
        for line in selected_lines:
            df = extract_range_graph_data(file_path, line, selected_variable)
            if not df.empty:
                df_part = pd.DataFrame({'z': df['z'], f"{line}_{selected_stat}": df[selected_stat]})
                combined_df = df_part if combined_df.empty else pd.merge(combined_df, df_part, on='z', how='outer')
        return combined_df
    except Exception as e:
        print(f"Data extraction error: {e}")
        return pd.DataFrame()

# ========== Callbacks ==========

def on_file_selection(state):
    if state.file_paths:
        state.file_lov = list(state.file_paths)
        state.Selected_file = state.file_lov[0]
        state.lines_lov = get_line_names(state.Selected_file)
        state.lines = []

def on_file_change(state):
    if state.file_paths:
        state.Selected_file = state.file_paths[0]
        state.lines_lov = get_line_names(state.Selected_file)
        state.lines = []

def change_category(state):
    if state.variable_category:
        state.variable_lov = list(variables_dict[state.variable_category].keys())
        state.variable = state.variable_lov[0] if state.variable_lov else ""

def process_selected_data(state):
    if not state.Selected_file or not state.lines or not state.variable:
        notify(state, "error", "Missing file, lines, or variable.")
        return

    selected_lines = state.lines if isinstance(state.lines, list) else [state.lines]
    result_df = extract_multiple_lines_data(state.Selected_file, selected_lines, state.variable, state.selected_statistic)
    result_df.columns = result_df.columns.astype(str)
    result_df = result_df.reset_index(drop=True)
    state.extracted_data = result_df
    state.data_available = not result_df.empty
    if state.data_available:
        print(f"Data extracted: {result_df.shape}")

# ========== GUI Layout ==========

@page()
def main():
    return Container(
        Text("# Post Sim result dashboard", mode="md", class_name="text-center mt-1"),
        Layout(columns="40 20 40", gap="20px")(
            Text(""),
            Image(LOGO_PATH, width="100%", height="100%", class_name="text-center")
        ),
        Container(
            Layout(columns="1 2 2", gap="10px")(
                Container(
                    Text("Select .sim file **From**", mode="md"),
                    FileSelector("file_paths", multiple=True, extensions=".sim,.Sim"),
                    Button("Process Selected Files", on_action=on_file_selection)
                ),
                Container(
                    Text("Select **FILES**", mode="md"),
                    Selector("file_paths", lov="file_lov", multiple=True, dropdown=True, on_change=on_file_change),
                    Button("Extract Lines", on_action=on_file_change)
                ),
                Container(
                    Text("Select **Line/s**", mode="md"),
                    Selector("lines", lov="lines_lov", multiple=True, dropdown=True)
                )
            ),
        ),
        Container(
            Layout(columns="1 2 2")(
                Text("Selected file is: {Selected_file}", mode="md"),
                Container(
                    Text("Select **Results Category**", mode="md"),
                    Selector("variable_category", lov="categories_lov", dropdown=True, on_change=change_category),
                    Text("Select results **variable**", mode="md"),
                    Selector("variable", lov="variable_lov", dropdown=True),
                    Text("Select **statistic**", mode="md"),
                    Selector("selected_statistic", lov=["min", "max", "mean"], dropdown=True),
                    Button("Extract Data", on_action=process_selected_data)
                )
            )
        ),
        Container(
            Text("**Extracted Data Table**", mode="md"),
            Table("extracted_data", width="100%", class_name="taipy-show-if:{data_available}")
        )
    )

# ========== Entry Point ==========

if __name__ == "__main__":
    initial_state = {
        "file_paths": [],
        "file_lov": [],
        "Selected_file": "",
        "lines": [],
        "lines_lov": [],
        "variable_category": variable_category[0],
        "categories_lov": categories_lov,
        "variable": "",
        "variable_lov": [],
        "selected_statistic": "mean",
        "extracted_data": pd.DataFrame(),
        "data_available": False
    }

    Gui(pages={"main": main}, state=initial_state).run(
        title="Orcaflex Results Viewer",
        dark_mode=False,
        use_reloader=True,
        port="auto"
    )
