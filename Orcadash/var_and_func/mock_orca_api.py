import random
import pandas as pd

class MockOrcFxAPI:
    def __init__(self, *args, **kwargs):
        self.objects = self._generate_mock_objects()

    def _generate_mock_objects(self):
        return [
            MockObject("Line1", "Line"),
            MockObject("Line2", "Line"),
            MockObject("Vessel1", "Vessel"),
        ]

    def __getitem__(self, key):
        for obj in self.objects:
            if obj.Name == key:
                return obj
        raise KeyError(f"Object '{key}' not found.")

    @property
    def otLine(self):
        return "Line"

class MockObject:
    def __init__(self, name, obj_type):
        self.Name = name
        self.type = obj_type

    def RangeGraph(self, variable, period):
        return MockRangeGraph()

class MockRangeGraph:
    def __init__(self):
        self.X = [i * 10 for i in range(10)]
        self.Min = [random.uniform(0, 10) for _ in range(10)]
        self.Max = [random.uniform(10, 20) for _ in range(10)]
        self.Mean = [random.uniform(5, 15) for _ in range(10)]

# To be used in the main script
def Model(file_path):
    print(f"Mocking OrcFxAPI.Model for file: {file_path}")
    return MockOrcFxAPI()

class PeriodNum:
    WholeSimulation = 0
