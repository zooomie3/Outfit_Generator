from pathlib import Path
import pandas as pd


class DataSet:
    """
    Creating a parent class that stores the CSV file path and loads the CSV into a dataframe.
    Both closet and weather data are coming from CSVs, read by pandas, and stored as DataFrames so this logic makes sense for the parent class.
    Closet and weather will inheret load_data(), get_data(), file_path, and df
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path) # stores file location inside the object
        self.df = None # because data hasn't been loaded yet

    def load_data(self): 
        """Reads the CSV file into a pandas DataFrame."""
        self.df = pd.read_csv(self.file_path) # stores CSV file in df
        return self.df

    def get_data(self):
        """Safe way to acces data, checking if CSV is loaded. Returns the DataFrame, loading it first if needed."""
        if self.df is None:
            self.load_data() # if CSV not loaded, this loads it anyway
        return self.df