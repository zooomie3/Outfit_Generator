import pandas as pd
from dataset import DataSet

class Weather(DataSet):
    """
    Child class representing the weather dataset.

    This class inherits from DataSet, so it has the ability to:
    - store the CSV file path
    - load the CSV into a pandas DataFrame
    - standardize column names
    - return the dataset safely with get_data()

    Weather adds weather-specific behavior:
    - extra cleaning for the weather dataset
    - looking up weather information for a specific date
    - converting temperature in celcius into a temperature category
    """

    def __init__(self, file_path):
        super().__init__(file_path) 

    def load_data(self):
        """
        Loads and cleans the weather dataset.
        This method first calls the parent class load_data() method to read the CSV file and standardize the column names 
        Also applies weather-specific cleaning:
        - converts date column into real date objects
        - removes rows with invalid dates
        - converts temp_celsius into numeric values
        - removes rows with invalid temperatures
        - removes duplicate dates

        Returns: pandas.DataFrame: The cleaned weather dataset.
        """
        df = super().load_data() # inherets from parent class

        # converting date strings into real python date objects
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date # removes invalid dates
            df = df.dropna(subset=["date"]) # removes rows were date is missing

        if "temp_celsius" in df.columns:
            df["temp_celsius"] = pd.to_numeric(df["temp_celsius"], errors="coerce") # converst temps to numeric
            df = df.dropna(subset=["temp_celsius"]) # removes rows where temp couldnt be converted

        if "date" in df.columns:
            df = df.drop_duplicates(subset=["date"], keep="first") # remove duplicate dates

        self.df = df.reset_index(drop=True) # index reset after cleaning rows
        return self.df

    def show_weather(self):
        """
        Prints the weather dataset; mainly useful for testing and checking whether the file is loaded correctly or not.
        """
        print(self.get_data()) # from parent class

    def classify_temperature(self, temp_c):
        """
        Converts a numeric temp in celsius to a temperature category.
        Categories:
            - below 10  -> COLD
            - 10 to <20 -> MILD
            - 20 to <27 -> WARM
            - 27+       -> HOT
        Parameters: temp_c (float): Temperature in degrees Celsius.
        Returns: str: One of COLD, MILD, WARM, or HOT.
        """
        if temp_c < 10:
            return "COLD"
        elif temp_c < 20:
            return "MILD"
        elif temp_c < 27:
            return "WARM"
        else:
            return "HOT"

    def get_temperature_for_date(self, date_str):
        """
        Returns the temperature category of a specific date.

        The method first tries to find an exact date match, and if that date isn't found, it uses the nearest previous date.
        If there is still no earlier date available, it falls back to the first row.

        Parameters: date_str (str)- date string in YYYY-MM-DD format.

        Returns string temp category for that date (COLD, MILD, WARM, or HOT).
        """
        df = self.get_data() # retrieve cleaned dataset
        target_date = pd.to_datetime(date_str).date() # convert string into date object

        # Try exact match first
        match = df[df["date"] == target_date]
        if not match.empty:
            temp_c = float(match.iloc[0]["temp_celsius"])
            return self.classify_temperature(temp_c)

        # If date is missing, use the nearest previous date
        previous = df[df["date"] < target_date]
        if not previous.empty:
            temp_c = float(previous.iloc[-1]["temp_celsius"])
            return self.classify_temperature(temp_c)

        # Final fallback is to use first row
        temp_c = float(df.iloc[0]["temp_celsius"])
        return self.classify_temperature(temp_c)

    def get_weather_for_date(self, date_str):
        """
        Returns the numeric temperature and weather condition for a certain date.
        This method first tries to find an exact date match, and if that date is not found, it uses the nearest previous date.
        If there is still no earlier date available, it falls back to the first row.

        Parameters: date_str (str): Date string, in YYYY-MM-DD format.

        Returns: tuple[float, str]containing:
            - temp_celsius: float
             - condition: str, normalized to uppercase
        """
        df = self.get_data()
        target_date = pd.to_datetime(date_str).date()

        # Try exact match first
        match = df[df["date"] == target_date]
        if not match.empty:
            row = match.iloc[0]
            temp_c = float(row["temp_celsius"])
            condition = str(row.get("condition", "")).strip().upper()
            return temp_c, condition

        # If date is missing, use nearest previous date
        previous = df[df["date"] < target_date]
        if not previous.empty:
            row = previous.iloc[-1]
            temp_c = float(row["temp_celsius"])
            condition = str(row.get("condition", "")).strip().upper()
            return temp_c, condition

        # Final fallback is to use first row
        row = df.iloc[0]
        temp_c = float(row["temp_celsius"])
        condition = str(row.get("condition", "")).strip().upper()
        return temp_c, condition
