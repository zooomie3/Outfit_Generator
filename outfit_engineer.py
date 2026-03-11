from __future__ import annotations

import random
from typing import Optional

import pandas as pd


# Determining the "required" and the "optional" categories of clothing.
# The requied categories need to be always present in an outfit while the optional categories can be included or not based on the weather and temperature conditions. 
REQUIRED_POSITIONS = ["TOP", "BOT", "SHO", "BAG"]
OPTIONAL_POSITIONS_DEFAULT = ["OUT", "LAY", "ACC", "HAT"]

# Cleaning the dataset
# Ensuring everything is in uppercase and without whitespace (ensuring consistency). 
def _normalize_str(x) -> str:
    return str(x).strip().upper()

def _ensure_position_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    This ensures a 'position' column exists in the DataFrame.
    If the category is missing/empty, infer from item_id prefix (TOP_01 -> TOP).
    """
    # Working on a copy in order to avoid changing/modyfing the orginial dataframe. 
    df = df.copy()

    # Columnns that have no position will be filled with empty string. 
    if "position" not in df.columns:
        df["position"] = ""

    # item_id is required because we may need to infer position from it
    if "item_id" not in df.columns:
        raise KeyError("build_outfit expected column 'item_id' in clothing_df")

    # Cleaning existing position column
    pos = df["position"].fillna("").astype(str).str.strip()

    # Rows that have no position
    needs_infer = pos.eq("")
    
    # For rows that have no position, infer from item_id
    inferred = (
        df.loc[needs_infer, "item_id"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.split("_", n=1)
        .str[0]
    )

    # put inferred position in blank rows
    df.loc[needs_infer, "position"] = inferred
    df["position"] = df["position"].apply(_normalize_str)

    # converts all possible names to standard name
    POSITION_MAP = {
        "TOP": "TOP",
        "BOTTOM": "BOT",
        "BOT": "BOT",
        "SHOES": "SHO",
        "SHOE": "SHO",
        "SHO": "SHO",
        "BAG": "BAG",
        "OUTER": "OUT",
        "OUT": "OUT",
        "LAYER": "LAY",
        "LAY": "LAY",
        "ACCESSORY": "ACC",
        "ACC": "ACC",
        "HAT": "HAT",
    }

    df["position"] = df["position"].replace(POSITION_MAP)
    return df


def _pick_one(pool: pd.DataFrame, position: str, rng: random.Random) -> pd.DataFrame:
    """Picks one row from a pool for a given position which then returns a single-row DataFrame. Raises ValueError if no items for that position."""
    position_pool = pool[pool["position"] == position]

    # If there are no items for the specific postion, raise a ValueError. 
    if position_pool.empty:
        raise ValueError(f"No items available for position: {position}")

    idx = rng.choice(position_pool.index.tolist())
    return position_pool.loc[[idx]]


def _pick_required_with_fallback(
    filtered_df: pd.DataFrame,
    full_df: pd.DataFrame,
    position: str,
    rng: random.Random,
) -> pd.DataFrame:
    """
    For required positions:
    1. try filtered items
    2. if none, fall back to the full closet
    3. if still none, raise an error
    """
    # Trying to pick from the filtered closet first. 
    filtered_pool = filtered_df[filtered_df["position"] == position]

    # For the filtered item exists, pick one from the filtered closet.
    if not filtered_pool.empty:
        idx = rng.choice(filtered_pool.index.tolist())
        return filtered_pool.loc[[idx]]

    full_pool = full_df[full_df["position"] == position]
    
    # If no filtered item exists but there are items in the full closet, print a warning and pick one from the full closet as a fallback.
    if not full_pool.empty:
        print(f"Warning: no filtered items for {position}, using fallback from full closet.")
        idx = rng.choice(full_pool.index.tolist())
        return full_pool.loc[[idx]]
    
    # If no items exist at all for the required position, raise an error because we can't build a valid outfit.
    raise ValueError(f"No items exist at all for required position: {position}")


def build_outfit(
    filtered_df: pd.DataFrame,
    full_df: pd.DataFrame,
    temp_celsius: float,
    weather_condition: str,
    *,
    include_optional: bool = True,
    optional_prob: float = 0.5,
    seed: Optional[int] = None,
) -> pd.DataFrame:

    """
    Builds an outfit based on the filtered and full DataFrames, temperature, and weather conditions.
    Required positions:
        TOP, BOT, SHO, BAG
    Weather condition, logic for OUT items:
        - If cold (<= 10°C): require OUT
        - If rainy: require OUT
    """
    if filtered_df is None or len(filtered_df) == 0:
        print("Warning: filtered_df is empty, required items will be chosen from full_df fallback.")

    if full_df is None or len(full_df) == 0:
        raise ValueError("build_outfit received an empty full_df")
    
    # Creating a random generator (the seed allows for reproducibility of the results).
    rng = random.Random(seed)

    # Ensuring the position column is cleaned and standardized in both DataFrames. 
    # If the filtered_df is empty or None, an empty DataFrame with the same columns as full_df will be created to avoid errors in the outfit building process.
    filtered_df = _ensure_position_column(filtered_df if filtered_df is not None else pd.DataFrame(columns=full_df.columns))
    full_df = _ensure_position_column(full_df)

    # Normalizing the weather condition string for consistency. 
    wc = _normalize_str(weather_condition)

    required_positions = list(REQUIRED_POSITIONS)
    optional_positions = list(OPTIONAL_POSITIONS_DEFAULT)

    # Setting up the requirement for OUT position for when the temperature is equal or under 10 Celsius degrees or when it is raining. 
    if temp_celsius <= 10:
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    if "RAIN" in wc:
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    outfit_parts: list[pd.DataFrame] = []

    # For each required position, try to poick from the filtered closet first if not possible fallnack to full_df. 
    for pos in required_positions:
        outfit_parts.append(_pick_required_with_fallback(filtered_df, full_df, pos, rng))

    # For optional positions only choose from the filtered closet (filtered_df). 
    if include_optional:
        # Removing any optional positions that are already in the required positions (removes duplication). 
        optional_positions = [p for p in optional_positions if p not in required_positions]

        for pos in optional_positions:
            pool = filtered_df[filtered_df["position"] == pos]
            if pool.empty:
                continue

            if rng.random() < optional_prob:
                idx = rng.choice(pool.index.tolist())
                outfit_parts.append(pool.loc[[idx]])

    # Combining all the selected parts into a single DataFrame which represents the final outfit. 
    outfit_df = pd.concat(outfit_parts, ignore_index=True)

    # Removing any possible duplicates (sefety check). 
    if "item_id" in outfit_df.columns:
        outfit_df = outfit_df.drop_duplicates(subset=["item_id"], keep="first").reset_index(drop=True)

    # Returning the final outfit DataFrame. 
    return outfit_df