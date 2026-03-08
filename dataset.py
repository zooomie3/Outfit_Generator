from pathlib import Path
import pandas as pd


class DataSet:
    """
    Creating a parent class that stores the CSV file path andloads the CSV into a dataframe.
    Both closet and weather data are coming from CSVs, read by pandas, and stored as DataFrames so this logic makes snese for a parent class.
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path) 
        self.df = None

    def load_data(self):
        """Loads the CSV file into a pandas DataFrame."""
        self.df = pd.read_csv(self.file_path)
        return self.df

    def get_data(self):
        """Returns the DataFrame, loading it first if needed."""
        if self.df is None:
            self.load_data()
        return self.df