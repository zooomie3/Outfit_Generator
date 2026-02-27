import pandas as pd

def filter_by_occasion(clothing_df, occasion, occasion_dict):
    """
    Removes clothing items that are not valid for the given occasion.
    Returns a filtered DataFrame.
    """
    allowed_items = occasion_dict.get(occasion, [])
    return clothing_df[clothing_df["item_name"].isin(allowed_items)].copy()


def filter_by_temperature(clothing_df, temperature):
    """
    Removes clothing items that are not suitable for the given temperature.
    Returns a filtered DataFrame.
    """
    return clothing_df[
        (clothing_df["min_temp"] <= temperature) &
        (clothing_df["max_temp"] >= temperature)
    ].copy()
