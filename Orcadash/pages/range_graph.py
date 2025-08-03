try:
    import OrcFxAPI
except ImportError:
    from var_and_func import mock_orca_api as OrcFxAPI
    MOCK_MODE = True
else:
    MOCK_MODE = False
import taipy.gui.builder as tgb
from taipy.gui import State, Gui, notify
import pandas as pd
from datetime import datetime
import sys
import os
from typing import List
import plotly.graph_objects as go
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from var_and_func.variables import variables_dict, get_variable_units
from var_and_func.functions import get_line_names, extract_multiple_lines_data

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Orcadash.png')

# Initial state
file_paths = []
selected_files = []
lines = []
lines_lov = []
variable_category = list(variables_dict.keys())
selected_category = list(variables_dict.keys())[0]
variable = ""
variable_lov = []
extracted_data = pd.DataFrame()
data_available = False
selected_statistic = "mean"
figure = go.Figure()
table_columns = []
is_loading = False
plot_mode = "lines+markers"
chart_title = "Range Graph"

def update_variable_lov(state: State):
    """Update the variable list based on the selected category."""
    category_variables = list(variables_dict.get(state.selected_category, {}).keys())
    state.variable_lov = category_variables
    if category_variables:
        state.variable = category_variables[0]

def on_file_select(state: State):
    """Callback when a file is selected."""
    if MOCK_MODE and not state.file_paths:
        state.file_paths = ["mock_file_1.sim", "mock_file_2.sim"]
        notify(state, "info", "Using mock files for demonstration.")

    if state.file_paths:
        state.selected_files = state.file_paths
        if isinstance(state.selected_files, str):
            state.selected_files = [state.selected_files]

        lines = []
        for file in state.selected_files:
            try:
                lines.extend(get_line_names(file, OrcFxAPI))
            except Exception as e:
                notify(state, "error", f"Failed to read lines from {file}: {e}")
        state.lines_lov = sorted(list(set(lines)))

def process_data(state: State):
    """Process the selected data and generate the graph and table."""
    if not state.selected_files:
        notify(state, "error", "Please select one or more .sim files.")
        return
    if not state.lines:
        notify(state, "error", "Please select one or more lines.")
        return
    if not state.variable:
        notify(state, "error", "Please select a variable.")
        return

    state.is_loading = True
    state.data_available = False

    try:
        all_data = []
        for file in state.selected_files:
            df = extract_multiple_lines_data(file, state.lines, state.variable, OrcFxAPI, state.selected_statistic)
            if not df.empty:
                # Add file identifier to each column except 'z'
                for col in df.columns:
                    if col != 'z':
                        df.rename(columns={col: f"{os.path.basename(file)} - {col}"}, inplace=True)
                all_data.append(df)

        if not all_data:
            notify(state, "warning", "No data could be extracted for the selected inputs.")
            state.is_loading = False
            return

        # Merge dataframes
        merged_df = all_data[0]
        for i in range(1, len(all_data)):
            merged_df = pd.merge(merged_df, all_data[i], on='z', how='outer')

        state.extracted_data = merged_df.sort_values(by='z').reset_index(drop=True)
        state.table_columns = [{"name": col, "id": col} for col in state.extracted_data.columns]
        state.figure = create_range_graph_figure(state)
        state.data_available = True
        notify(state, "success", "Data processed successfully!")

    except Exception as e:
        notify(state, "error", f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        state.is_loading = False


def create_range_graph_figure(state: State):
    """Create a Plotly figure for the range graph data."""
    df = state.extracted_data
    statistic = state.selected_statistic
    variable_name = state.variable

    fig = go.Figure()

    for col in df.columns:
        if col != 'z':
            fig.add_trace(go.Scatter(
                x=df['z'],
                y=df[col],
                name=col,
                mode=state.plot_mode
            ))

    units = get_variable_units(variable_name)
    yaxis_title = f"{variable_name} ({statistic.capitalize()})"
    if units:
        yaxis_title += f" ({units})"

    fig.update_layout(
        title=state.chart_title,
        xaxis_title="Arc Length (m)",
        yaxis_title=yaxis_title,
        legend_title="File - Line",
        hovermode="x unified",
        height=600,
        template="plotly_dark"
    )
    return fig

def export_to_csv(state: State):
    """Export the extracted data to a CSV file."""
    if not state.extracted_data.empty:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extracted_data_{timestamp}.csv"
        state.extracted_data.to_csv(filename, index=False)
        notify(state, "success", f"Data exported to {filename}")

# Main GUI page
with tgb.Page() as page:
    tgb.text("# OrcaFlex Data Visualizer", mode="md", class_name="h1 text-center")

    with tgb.layout("1", class_name="card"):
        with tgb.expandable(title="Configuration", expanded=True):
            with tgb.layout("1 1 1", gap="1rem"):
                tgb.file_selector(
                    content="{file_paths}",
                    multiple=True,
                    extensions=".sim,.Sim",
                    label="Select .sim Files",
                    on_action=on_file_select,
                    class_name="fullwidth"
                )
                tgb.selector(
                    value="{lines}",
                    lov="{lines_lov}",
                    multiple=True,
                    label="Select Lines",
                    dropdown=True,
                    class_name="fullwidth"
                )
                tgb.selector(
                    value="{selected_category}",
                    lov="{variable_category}",
                    label="Variable Category",
                    dropdown=True,
                    on_change=update_variable_lov,
                    class_name="fullwidth"
                )
            with tgb.layout("1 1", gap="1rem"):
                tgb.selector(
                    value="{variable}",
                    lov="{variable_lov}",
                    label="Variable",
                    dropdown=True,
                    class_name="fullwidth"
                )
                tgb.selector(
                    value="{selected_statistic}",
                    lov=["min", "max", "mean"],
                    label="Statistic",
                    dropdown=True,
                    class_name="fullwidth"
                )
            tgb.button("Generate Visualization", on_action=process_data, class_name="btn btn-primary fullwidth")

    with tgb.part(render="{is_loading}", class_name="card text-center"):
        tgb.text("Loading data, please wait...", mode="md")

    with tgb.part(render="{data_available}"):
        with tgb.expandable(title="Chart Customization", expanded=False, class_name="card"):
            with tgb.layout("1 1", gap="1rem"):
                tgb.input("{chart_title}", label="Chart Title")
                tgb.selector(value="{plot_mode}", lov=["lines", "markers", "lines+markers"], label="Plot Mode", dropdown=True)
            tgb.button("Update Chart", on_action=create_range_graph_figure)

        with tgb.expandable(title="Chart", expanded=True, class_name="card"):
            tgb.chart(figure="{figure}")

        with tgb.expandable(title="Data Table", expanded=False, class_name="card"):
            tgb.table(data="{extracted_data}", columns="{table_columns}", page_size=10, class_name="table-striped")
            tgb.button("Export to CSV", on_action=export_to_csv, class_name="btn btn-secondary")

if __name__ == "__main__":
    gui = Gui(page=page)
    #gui.on_init = on_init
    update_variable_lov(gui)
    if MOCK_MODE:
        notify(gui, "info", "Running in mock mode. OrcFxAPI not found.")
    gui.run(
        title="OrcaFlex Data Visualizer",
        dark_mode=True,
        debug=True,
        use_reloader=True,
        margin="1em",
        css_file="style.css"
    )
