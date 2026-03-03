from pathlib import Path 
import pandas as pd

# This file contains functions to load and clean data from weather.csv and closet.csv.
# It also includes helper functions to get temperature categories and weather conditions for specific dates.
def _standardize_columns(df):
    df.columns = (
        df.columns
        .str.strip() # Remove leading/trailing whitespace from column names
        .str.lower() # Convert to lowercase for consistency
        .str.replace(r"\s+", "_", regex=True)          # Replace spaces with underscores
        .str.replace(r"[^0-9a-zA-Z_]+", "_", regex=True)  # Replace non-alphanumeric characters with underscores
        .str.strip("_") # Remove leading/trailing underscores that may have been introduced
    )
    return df 


# Temperature Categories (Celsius)
# List of tuples: (category_name, lower_bound, upper_bound)
# float("-/+inf") is used to cover all possible temperature values so we don’t need arbitrary minimum/maximum temperatures
TEMP_CATEGORIES = [
    ("COLD", float("-inf"), 10),
    ("MILD", 10, 20),
    ("WARM", 20, 27),
    ("HOT", 27, float("inf")),
]

# Converting temperature to categories 
def _classify_temperature(temp_c: float) -> str:
    """
    Convert Celsius temperature to: COLD / MILD / WARM / HOT
    """
    for name, lower, upper in TEMP_CATEGORIES:
        if lower <= temp_c < upper: 
            return name # Function will return the category name as soon as it finds a match, so we don't need to check all categories once a match is found

    return "MILD"  # Fallback safety in case our range doesn't cover all temperatures


def load_weather(path: str | Path = "Fashionista/weather.csv") -> pd.DataFrame:
    """
    Loads and cleans weather data.
    Expected columns after cleaning: date, temp_celsius, condition
    """

    df = pd.read_csv(Path(path))
    df = _standardize_columns(df)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date # Convert to date only (no time) and coerce changes errors to NaT (missing date)
        df = df.dropna(subset=["date"]) #removes rows with NaT 

    if "temp_celsius" in df.columns:
        df["temp_celsius"] = pd.to_numeric(df["temp_celsius"], errors="coerce") # Convert to numeric and coerce errors to NaN (missing temperature)
        df = df.dropna(subset=["temp_celsius"]) # Remove rows where temperature couldn't

    if "date" in df.columns:
        df = df.drop_duplicates(subset=["date"], keep="first")
    return df.reset_index(drop=True)


def load_clothing(path: str | Path ="Fashionista/closet.csv") -> pd.DataFrame:
    """
    Load and clean clothing data.
    Expected columns: item_id, position, type, style, weather_temp,weather_condition
    """
    path = Path(path)

    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    df = _standardize_columns(df)

    # Remove unnamed columns (like Unnamed: 0)
    df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]

    # Remove fully empty rows
    df = df.dropna(how="all")

    # Strip whitespace ONLY in text columns (prevents numbers becoming strings)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    return df.reset_index(drop=True)


def get_temperature_for_date(date_str, weather_df: pd.DataFrame) -> str:
    """
    Given a date string (YYYY-MM-DD), return temperature category: COLD / MILD / WARM / HOT
    """

    target_date = pd.to_datetime(date_str).date()

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


def get_weather_for_date(date_str: str, weather_df: pd.DataFrame) -> tuple[float, str]:
    """
    Returns (temp_celsius, condition) for a date.
    This is useful for outfit-building logic that needs numeric temperature.
    """
    target_date = pd.to_datetime(date_str).date()

    match = weather_df[weather_df["date"] == target_date]
    if not match.empty:
        row = match.iloc[0]
        temp_c = float(row["temp_celsius"])
        condition = str(row.get("condition", "")).strip().upper()
        return temp_c, condition

    previous = weather_df[weather_df["date"] < target_date]
    if not previous.empty:
        row = previous.iloc[-1]
        temp_c = float(row["temp_celsius"])
        condition = str(row.get("condition", "")).strip().upper()
        return temp_c, condition

    row = weather_df.iloc[0]
    temp_c = float(row["temp_celsius"])
    condition = str(row.get("condition", "")).strip().upper()
    return temp_c, condition
