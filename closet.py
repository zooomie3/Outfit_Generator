#importing all closet data 
import pandas as pd

class Closet:
    def __init__(self, csv_path):
        self.items = pd.read_csv(csv_path)

    def show_items(self):
            print(self.items)
