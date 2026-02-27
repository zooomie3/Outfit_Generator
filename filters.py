import pandas as pd

def _normalize_key(s: str) -> str:
    """Normalize user input like 'Family dinner' -> 'family_dinner'."""
    return str(s).strip().lower().replace(" ", "_")

def filter_by_occasion(clothing_df: pd.DataFrame, occasion: str, occasion_dict: dict) -> pd.DataFrame:
    """
    Removes clothing items that are not valid for the given occasion.
    Requires clothing_df column:
        item_id
    Requires occasion_dict (OCCASION_RULES):
        occasion_key -> list of item_ids
    """
    occasion_key = _normalize_key(occasion)
    allowed_items = occasion_dict.get(occasion_key, [])

    # If occasion doesn't exist, return unchanged so you can still test the pipeline
    if not allowed_items:
        return clothing_df.copy()

    if "item_id" not in clothing_df.columns:
        raise KeyError("filter_by_occasion expected column 'item_id' in clothing_df")

    return clothing_df[clothing_df["item_id"].astype(str).str.upper().isin([x.upper() for x in allowed_items])].copy()

#
def filter_by_temperature_category(clothing_df: pd.DataFrame, temp_category: str) -> pd.DataFrame:
    """
    Filters clothing items that support the given temperature category.
    Uses the 'weather_temp' column from your CSV.
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

if __name__ == "__main__":
    # --- quick sanity test for this file only ---
    from data_loader import load_clothing, load_weather, get_temperature_for_date, get_weather_for_date
    from occasion_rules import OCCASION_RULES

    print("\n=== filters.py SELF-TEST ===")

    # ✅ adjust paths if needed (based on your setup)
    clothing_df = load_clothing("data/closet.csv")
    weather_df = load_weather("data/weather.csv")

    print("Clothing rows:", len(clothing_df))
    print("Clothing columns:", clothing_df.columns.tolist())
    print("Weather rows:", len(weather_df))

    test_date = "2026-02-27"
    test_occasion = "casual"

    temp_cat = get_temperature_for_date(test_date, weather_df)
    temp_c, condition = get_weather_for_date(test_date, weather_df)

    print("\nTest date:", test_date)
    print("Temp (C):", temp_c)
    print("Temp category:", temp_cat)
    print("Condition:", condition)

    # Run each filter separately so you can see which one kills the data
    df_occ = filter_by_occasion(clothing_df, test_occasion, OCCASION_RULES)
    print("\nRows after occasion filter:", len(df_occ))

    df_temp = filter_by_temperature_category(clothing_df, temp_cat)
    print("Rows after temperature filter:", len(df_temp))

    df_weather = filter_by_weather_condition(clothing_df, condition)
    print("Rows after weather filter:", len(df_weather))

    # Combine filters
    df_all = filter_by_weather_condition(
        filter_by_temperature_category(
            filter_by_occasion(clothing_df, test_occasion, OCCASION_RULES),
            temp_cat
        ),
        condition
    )
    print("Rows after ALL filters:", len(df_all))

    if len(df_all) > 0:
        cols = [c for c in ["item_id", "position", "temperature_category", "weather_temp", "weather_condition", "style"] if c in df_all.columns]
        print("\nSample filtered items:")
        print(df_all[cols].head(10))

    print("\n=== END SELF-TEST ===\n")