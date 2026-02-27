#importing all closet data 
import pandas as pd
from pathlib import Path

class Closet:
    def __init__(self, csv_path: str | Path):
        self.items = pd.read_csv(Path(csv_path))

    def show_items(self):
        print(self.items)

