#Closet
#importing all closet data 
import pandas as pd

class Closet:
    def __init__(self, csv_path):
        self.items = pd.read_csv(csv_path)

    def show_items(self):
            print(self.items)
from pathlib import Path 
import pandas as pd

# Temperature Categories (Celsius)
# List of tuples: (category_name, lower_bound, upper_bound)
# float("-/+inf") is used to cover all possible temperature values so we don’t need arbitrary minimum/maximum temperatures
TEMP_CATEGORIES = [
    ("COLD", float("-inf"), 10),
    ("MILD", 10, 20),
    ("WARM", 20, 27),
    ("HOT", 27, float("inf")),
]

def _standardize_columns(df):
    """
    Making column names lowercase and cleaning up spaces so everyone on the team can have consistency.
        .str.strip() removes leading and trailing whitespace
        .str.lower() converts to lowercase
        .str.replace(" ", "_") replaces spaces with underscores for easier access in code
    """
    df.columns = (
        df.columns
        .str.strip() 
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

# Converting temperature to categories 
def _classify_temperature(temp_c):
    """
    Convert Celsius temperature to: COLD / MILD / WARM / HOT
    """
    for name, lower, upper in TEMP_CATEGORIES:
        if lower <= temp_c < upper: 
            return name # Function will return the category name as soon as it finds a match, so we don't need to check all categories once a match is found

    return "MILD"  # Fallback safety in case our range doesn't cover all temperatures


def load_weather(path="weather.csv"):
    """
    Loads and cleans weather data.

    Expected columns after cleaning:
        date
        temp_celsius
        condition
        precip_mm
        humidity_%
        wind_speed_kmh
        uv_index
    """

    df = pd.read_csv(Path(path))
    df = _standardize_columns(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date # Convert to date only (no time) and coerce changes errors to NaT (missing date)
    df = df.dropna(subset=["date"]) #removes rows with NaT 

    # Ensures temperature column is numeric
    df["temp_celsius"] = pd.to_numeric(df["temp_celsius"], errors="coerce")
    df = df.dropna(subset=["temp_celsius"]) # Remove rows where temperature couldn't be converted to a number

    # Removing duplicate dates
    df = df.drop_duplicates(subset=["date"], keep="first")

    return df.reset_index(drop=True) # Reseting index after dropping rows to keep it sequential


def load_clothing(path="Fashionista/closet.csv"):
    """
    Load and clean clothing data.

    Expected columns:
        item_id
        position
        type
        style
        weather_temp
        weather_condition
    """

    path = Path(path)

    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    df = _standardize_columns(df)

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains("^unnamed")]

    # Remove fully empty rows
    df = df.dropna(how="all")

    # Strip whitespace from all columns
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df.reset_index(drop=True) # Reseting index after dropping rows 


def get_temperature_for_date(date, weather_df):
    """
    Given a date string (YYYY-MM-DD), return temperature category:
        COLD / MILD / WARM / HOT
    """

    target_date = pd.to_datetime(date).date()

    # Try exact match
    match = weather_df[weather_df["date"] == target_date]

    if not match.empty:
        temp_c = float(match.iloc[0]["temp_celsius"])
        return _classify_temperature(temp_c)

    # If exact date not found → use nearest previous date
    previous = weather_df[weather_df["date"] < target_date]

    if not previous.empty:
        temp_c = float(previous.iloc[-1]["temp_celsius"])
        return _classify_temperature(temp_c)

    # Final fallback is to use first row to prevent any crashes 
    temp_c = float(weather_df.iloc[0]["temp_celsius"])
    return _classify_temperature(temp_c)
