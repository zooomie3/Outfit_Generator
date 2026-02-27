#CLOSET
#importing all closet data 
import pandas as pd

class Closet:
    def __init__(self, csv_path):
        self.items = pd.read_csv(csv_path)

    def show_items(self):
            print(self.items)
from pathlib import Path 
import pandas as pd

# DATA LOADER 
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

# OCCASION_RULES
    # Identifying occasions and giving them output
occasion_rules = {
    "night_out": ["BOT_02", "TOP_07", "TOP_05", "SHO_04", "SHO_06", "BAG_01", "BOT_10", "TOP_09", "OUT_02", "TOP_14", "OUT_01"],
    "family dinner": ["TOP_12", "BOT_10", "TOP_11", "TOP_03", "TOP_04", "TOP_09", "BOT_03", "SHO_03", "OUT_01", "TOP_10", "SHO_10"],
    "casual": ["BOT_10", "SHO_03", "TOP_02", "TOP_06", "TOP_13", "TOP_12", "TOP_11", "BOT_11", "TOP_08", "TOP_14", "SHO_06", "BAG_03", "BAG_06", "TOP_10", "SHO_10"],
    "gym": ["TOP_02", "TOP_13", "BOT_05", "BOT_08", "BOT_09", "SHO_03", "SHO_08", "BAG_02", "BOT_07"], 
    "formal": ["BOT_12", "LAY_06", "OUT_04", "TOP_10", "BOT_03", "SHO_04", "SHO_05", "SHO_06", "BAG_04", "ACC_04"],
    "festival": ["HAT_06", "OUT_06", "SHO_09", "HAT_05", "OUT_03", "TOP_06", "TOP_07", "TOP_09", "BOT_06", "BOT_11", "BOT_04", "BOT_12", "SHO_02", "SHO_03", "SHO_06", "ACC_02", "BAG_06"], 
    "beach": ["TOP_01", "BOT_01", "BOT_06", "TOP_05", "SHO_01", "SHO_02", "ACC_02", "ACC_03", "BAG_05"]
}

# add outerwear later as well
# add accessoiries in excel file/csv
# hats are missing!! 1-4
# layers are missing
# how are we going to add different outerwear clothes... random?

# FILTER 
import pandas as pd

def filter_by_occasion(clothing_df, occasion, occasion_dict):
    """
    Removes clothing items that are not valid for the given occasion.
    Returns a filtered DataFrame.
    """
    allowed_items = occasion_dict.get(occasion, [])
    return clothing_df[clothing_df["item_id"].isin(allowed_items)].copy()


def filter_by_temperature(clothing_df, temperature):
    """
    Removes clothing items that are not suitable for the given temperature.
    Returns a filtered DataFrame.
    """
    return clothing_df[
        (clothing_df["min_temp"] <= temperature) &
        (clothing_df["max_temp"] >= temperature)
    ].copy()
copy()

# OUTFIT ENGINEER 
import random
import pandas as pd

def build_outfit(filtered_df, temperature, weather_condition):

    outfit_items = []

    required_types = ["top", "bottoms", "shoes"]
    optional_types = ["accessoires", "bags", "hats", "outerwear", "layers"]

    # Temperature logic
    if temperature <= 10:
        required_types.append("outerwear")
        required_types.append("layers")

    if temperature > 27:
        if "outerwear" in optional_types:
            optional_types.remove("outerwear")
        if "layers" in optional_types:
            optional_types.remove("layers")

    # Rain logic
    if weather_condition == "rainy":
        required_types.append("OUT_03")
        required_types.append("SHO_07")

        # Remove normal shoes when wearing boots
        if "shoes" in required_types:
            required_types.remove("shoes")

    if weather_condition == "sunny":
        optional_types.append("sunglasses")
    
    # Required categories
    for clothing_type in required_types:
        items_of_type = filtered_df[
            filtered_df["position"] == clothing_type
        ]

        if items_of_type.empty:
            print(f"No {clothing_type} available!")
            return None

        selected_item = items_of_type.sample(1)
        outfit_items.append(selected_item)

    # Optional categories
    for clothing_type in optional_types:
        items_of_type = filtered_df[
            filtered_df["position"] == clothing_type
        ]

        if not items_of_type.empty:
            if random.random() > 0.5:
                selected_item = items_of_type.sample(1)
                outfit_items.append(selected_item)

    final_outfit = pd.concat(outfit_items, ignore_index=True)

    return final_outfit


weather_df = pd.read_csv("weather.csv")
clothing_df = pd.read_excel("clothing.xlsx")

temperature = 12
weather_condition = "rainy"

filtered_df = clothing_df  # After your filtering steps

outfit = build_outfit(filtered_df, temperature, weather_condition)

print(outfit)

