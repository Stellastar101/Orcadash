import OrcFxAPI
import pandas as pd
#import variables from variables

file_paths = [
    #r"C:\Users\Admin\Desktop\Dyneema_rope_analysis\Case01_1in20_K5_Dyneema.sim",
    #r"C:\Users\Admin\Desktop\Dyneema_rope_analysis\Case01_1in20_K5_Nylon&HSPP.sim",
    #r"C:\Users\MK\Desktop\Orcaflex 9.7\Orcaflex Examples\C Moorings\C05 Single Point Mooring\C05 Single Point Mooring.sim",
    #r"C:\Users\MK\Desktop\Orcaflex 9.7\Orcaflex Examples\C Moorings\C07 Metocean Buoy in Deep Water\C07 Metocean Buoy in Deep Water.sim",
     r"C:\Users\MK\Desktop\Orcaflex 9.7\Orcaflex Examples\C Moorings\C07 Metocean Buoy in Deep Water\C07 Metocean Buoy in Deep Water.sim"
]
def get_objects(file_path):
    """Load the OrcaFlex model and retrieve the names of all line objects."""
    try:
        model = OrcFxAPI.Model(file_path)
        line_names = [obj.Name for obj in model.objects if obj.type == OrcFxAPI.otLine]
        return line_names
    except Exception as e:
        print(f"Error loading file: {e}")
        return []
    

def extract_range_graph_data(self, file_path: str, line_name: str, variable: str) -> pd.DataFrame:
        """Extract range graph data from a file for a specific line and variable."""
        try:
            model = OrcFxAPI.Model(file_path)
            line = model[line_name]
            period = OrcFxAPI.PeriodNum.WholeSimulation
            rg = line.RangeGraph(variable, period)

            return pd.DataFrame({
                'z': rg.X,
                'min': rg.Min,
                'max': rg.Max,
                'mean': rg.Mean
            })
        except Exception as e:
            raise RuntimeError(f"Error extracting data from {line_name}: {str(e)}")


variable = "Effective Tension"

for files in file_paths:
    file = files
    lines = get_objects(files)
    for line in lines:
        print(line)
        selected_variable= "Effective tension"
        data  = extract_range_graph_data(file_path=file,selected_line=lines, selected_variable="Effective tension")

#extract_range_graph_data(file_path=file_paths, selected_line="Mooring", selected_variable="Effective tension")
extract_range_graph_data(
    file_path=file_paths,
    selected_line="Mooring",
    selected_variable="Wall Tension"
)
