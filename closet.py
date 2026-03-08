from dataset import DataSet
from filters import (
    filter_by_occasion,
    filter_by_temperature_category,
    filter_by_weather_condition,
)
from occasion_rules import OCCASION_RULES


class Closet(DataSet):
    """
    Child class representing the closet dataset.

    This class inherits from DataSet, so it has the ability to:
    - store the CSV file path
    - load the CSV into a pandas DataFrame
    - standardize column names
    - return the dataset safely with get_data()

    Closet adds clothing-specific behavior:
    - extra cleaning for the closet dataset
    - filtering items by occasion
    - filtering items by temperature category
    - filtering items by weather condition
    """
    def __init__(self, file_path):
        super().__init__(file_path)

    def load_data(self):
        """
        Loads and cleans the closet dataset.
        This method first calls the parent class load_data() method to read the CSV file and standardize column names.

        It also applies closet-specific cleaning:
        - removes unnamed columns
        - removes fully empty rows
        - strips extra whitespace from text columns

        Returns: pandas.DataFrame: The cleaned closet dataset.
        """
        df = super().load_data()

        df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]
        df = df.dropna(how="all")

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).str.strip()

        self.df = df.reset_index(drop=True)
        return self.df

    def show_items(self):
        """Prints closet dataset"""
        print(self.get_data())

    def filter_for_occasion(self, occasion):
        """
        Filters closet items that are suitable for a given occasion.
        Parameters: occasion- the occasion chosen by the user
        Returns: pandas.DataFrame: filtered DataFrame containing only items that match the imported occasion rules.
        """
        df = self.get_data()
        return filter_by_occasion(df, occasion, OCCASION_RULES)

    def filter_for_temperature(self, temp_category):
        """
        Filters closet items by temperature category.
        Parameters: temp_category- such as COLD, MILD, WARM, or HOT.
        Returns: pandas.DataFrame: filtered DataFrame containing only items suitable for that temperature category.
        """
        df = self.get_data()
        return filter_by_temperature_category(df, temp_category)

    def filter_for_weather(self, weather_condition):
        """
        Filters closet items by weather condition.
        Parameters: weather_condition- such as RAIN, SUNNY, WINDY, etc.
        Returns: pandas.DataFrame: filtered DataFrame containing only items suitable for that weather condition.
        """
        df = self.get_data()
        return filter_by_weather_condition(df, weather_condition)
    
