import pandas as pd
from typing import List

def get_line_names(file_path: str, orca_api) -> List[str]:
    """Load the OrcaFlex model and retrieve the names of all line objects."""
    try:
        model = orca_api.Model(file_path)
        return [obj.Name for obj in model.objects if obj.type == orca_api.otLine]
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

def extract_range_graph_data(file_path: str, line_name: str, variable: str, orca_api) -> pd.DataFrame:
    """Extract range graph data from a file for a specific line and variable."""
    try:
        model = orca_api.Model(file_path)
        line = model[line_name]
        period = orca_api.PeriodNum.WholeSimulation
        rg = line.RangeGraph(variable, period)

        return pd.DataFrame({
            'z': rg.X,
            'min': rg.Min,
            'max': rg.Max,
            'mean': rg.Mean,
            'line': line_name
        })
    except Exception as e:
        raise RuntimeError(f"Error extracting data from {line_name}: {str(e)}")

def extract_multiple_lines_data(file_path: str, selected_lines: List[str], selected_variable: str, orca_api, selected_stat: str = 'mean') -> pd.DataFrame:
    """Extract data for multiple lines and combine into a single DataFrame."""
    all_lines_data = []
    for line in selected_lines:
        try:
            df = extract_range_graph_data(file_path, line, selected_variable, orca_api)
            if not df.empty:
                line_df = df[['z', selected_stat]].copy()
                line_df.rename(columns={selected_stat: 'value'}, inplace=True)
                line_df['line'] = line
                all_lines_data.append(line_df)
        except Exception as e:
            print(f"Could not process line {line} in {file_path}: {e}")

    if not all_lines_data:
        return pd.DataFrame()

    combined_df = pd.concat(all_lines_data, ignore_index=True)
    pivot_df = combined_df.pivot_table(index='z', columns='line', values='value').reset_index()
    pivot_df.columns = ['z'] + [f"{line}_{selected_stat}" for line in pivot_df.columns[1:]]

    return pivot_df
