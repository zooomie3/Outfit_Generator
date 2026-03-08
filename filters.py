import pandas as pd

def _normalize_key(s: str) -> str:
    """Normalize user input like "Family dinner" turns into "family_dinner"."""
    return str(s).strip().lower().replace(" ", "_")

def filter_by_occasion(clothing_df: pd.DataFrame, occasion: str, occasion_dict: dict) -> pd.DataFrame:
    """
    Filters the clothing so that only clothes valid for a specific occasion remain.
    Parameters: clothing_df (closet dataset as dataframe), occasion user typed, the occassion rules
    """
    occasion_key = _normalize_key(occasion)
    allowed_items = occasion_dict.get(occasion_key, []) # find the item_id rules for each occassion

    # If occasion doesn't exist still return unchanged 
    if not allowed_items:
        return clothing_df.copy()

    if "item_id" not in clothing_df.columns:
        raise KeyError("filter_by_occasion expected column 'item_id' in clothing_df")

    return clothing_df[clothing_df["item_id"].astype(str).str.upper().isin([x.upper() for x in allowed_items])].copy()

#
def filter_by_temperature_category(clothing_df: pd.DataFrame, temp_category: str) -> pd.DataFrame:
    """
    Filters clothing items that support the given temperature category.
    Uses the 'weather_temp' column from the closet CSV.
    """

    if "weather_temp" not in clothing_df.columns:
        raise KeyError("Expected column 'weather_temp' in clothing_df")

    temp_category = str(temp_category).strip().upper()

    return clothing_df[
        clothing_df["weather_temp"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.contains(temp_category, regex=False)
    ].copy()

def filter_by_weather_condition(clothing_df: pd.DataFrame, weather_condition: str) -> pd.DataFrame:
    """
    Filters clothing items that match the given weather condition.
    Uses the 'weather_condition' column from the closet CSV.
    """
    if "weather_condition" not in clothing_df.columns:
        raise KeyError("Expected column 'weather_condition' in clothing_df")

    wc = str(weather_condition).strip().upper()

    return clothing_df[
        clothing_df["weather_condition"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.contains(wc, regex=False)
    ].copy()
