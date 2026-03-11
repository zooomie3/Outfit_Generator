import pandas as pd
from pathlib import Path


class DataSet:
    """
    Creating a parent class that stores the CSV file path and loads the CSV into a dataframe.
    Both closet and weather data are coming from CSVs, read by pandas, and stored as DataFrames so this logic makes sense for the parent class.
    Closet and weather will inheret load_data(), get_data(), file_path, and df
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path) # stores file location inside the object
        self.df = None # because data hasn't been loaded yet


    def _standardize_columns(self, df):
        df.columns = ( 
            df.columns # accesses list of column names
            .str.strip() # removes extra white space
            .str.lower() # makes everything lowercase
            .str.replace(r"\s+", "_", regex=True) # replace space with underscore
            .str.replace(r"[^0-9a-zA-Z_]+", "_", regex=True) # remove random characters
            .str.strip("_") # removes extra underscores
        )
        return df # returns dataframe with cleaned columns

    def load_data(self):
        """
        Reads CSV into DataFrame
        """
        df = pd.read_csv(self.file_path) # loads file
        df = self._standardize_columns(df) # cleans file
        self.df = df.reset_index(drop=True) # resets row numbers after cleaning (if rows wwere deleted)
        return self.df

    def get_data(self):
        """
        Makes sure CSV is loaded into DataFrame and returns it if not
        """
        if self.df is None:
            self.load_data() # if CSV not loaded, this loads it anyway
        return self.df