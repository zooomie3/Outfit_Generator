from __future__ import annotations

import random
from typing import Optional

import pandas as pd


# Required outfit slots
REQUIRED_POSITIONS = ["TOP", "BOT", "SHO", "BAG"]
OPTIONAL_POSITIONS_DEFAULT = ["OUT", "LAY", "ACC", "HAT"]

# Converts value into clean uppercase string
def _normalize_str(x) -> str:
    return str(x).strip().upper()

def _ensure_position_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures a 'position' column exists.
    If missing/empty, infer from item_id prefix (TOP_01 -> TOP).
    """
    df = df.copy()

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
    """Picks one row from a pool for a given position."""
    position_pool = pool[pool["position"] == position]

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
    filtered_pool = filtered_df[filtered_df["position"] == position]

    if not filtered_pool.empty:
        idx = rng.choice(filtered_pool.index.tolist())
        return filtered_pool.loc[[idx]]

    full_pool = full_df[full_df["position"] == position]

    if not full_pool.empty:
        print(f"Warning: no filtered items for {position}, using fallback from full closet.")
        idx = rng.choice(full_pool.index.tolist())
        return full_pool.loc[[idx]]

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
    Build an outfit from a filtered clothing dataframe, with fallback to full_df for required positions.
    Required positions:
        TOP, BOT, SHO, BAG
    Weather logic:
        - If cold (<= 10°C): require OUT
        - If rainy: require OUT
    """
    if filtered_df is None or len(filtered_df) == 0:
        print("Warning: filtered_df is empty, required items will be chosen from full_df fallback.")

    if full_df is None or len(full_df) == 0:
        raise ValueError("build_outfit received an empty full_df")

    rng = random.Random(seed)

    filtered_df = _ensure_position_column(filtered_df if filtered_df is not None else pd.DataFrame(columns=full_df.columns))
    full_df = _ensure_position_column(full_df)

    wc = _normalize_str(weather_condition)

    required_positions = list(REQUIRED_POSITIONS)
    optional_positions = list(OPTIONAL_POSITIONS_DEFAULT)

    if temp_celsius <= 10:
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    if "RAIN" in wc:
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    outfit_parts: list[pd.DataFrame] = []

    # Required positions: use fallback
    for pos in required_positions:
        outfit_parts.append(_pick_required_with_fallback(filtered_df, full_df, pos, rng))

    # Optional positions: only choose from filtered items
    if include_optional:
        optional_positions = [p for p in optional_positions if p not in required_positions]

        for pos in optional_positions:
            pool = filtered_df[filtered_df["position"] == pos]
            if pool.empty:
                continue

            if rng.random() < optional_prob:
                idx = rng.choice(pool.index.tolist())
                outfit_parts.append(pool.loc[[idx]])

    outfit_df = pd.concat(outfit_parts, ignore_index=True)

    if "item_id" in outfit_df.columns:
        outfit_df = outfit_df.drop_duplicates(subset=["item_id"], keep="first").reset_index(drop=True)

    return outfit_df


def print_outfit(outfit_df: pd.DataFrame) -> None:
    if outfit_df is None or outfit_df.empty:
        print("Outfit is empty.")
        return

    print("\n GENERATED OUTFIT ")
    print("-" * 40)

    for _, row in outfit_df.iterrows():
        print(
            f"{row.get('position','?'):>4} | "
            f"{row.get('item_id','?')} | "
            f"{row.get('category','')} | "
            f"{row.get('style','')}"
        )

    print("-" * 40)


if __name__ == "__main__":
    print("✅ Running outfit_engineer.py directly")

    full_test_df = pd.DataFrame([
        {"item_id": "TOP_01", "position": "TOP", "category": "T-Shirt", "style": "Casual"},
        {"item_id": "BOT_01", "position": "BOT", "category": "Jeans", "style": "Casual"},
        {"item_id": "SHO_01", "position": "SHO", "category": "Sneakers", "style": "Sporty"},
        {"item_id": "BAG_01", "position": "BAG", "category": "Tote", "style": "Casual"},
        {"item_id": "OUT_01", "position": "OUT", "category": "Jacket", "style": "Casual"},
    ])

    # Example filtered df missing BOT on purpose
    filtered_test_df = pd.DataFrame([
        {"item_id": "TOP_01", "position": "TOP", "category": "T-Shirt", "style": "Casual"},
        {"item_id": "SHO_01", "position": "SHO", "category": "Sneakers", "style": "Sporty"},
        {"item_id": "BAG_01", "position": "BAG", "category": "Tote", "style": "Casual"},
    ])

    outfit = build_outfit(
        filtered_df=filtered_test_df,
        full_df=full_test_df,
        temp_celsius=5,
        weather_condition="Rain",
        seed=42
    )

    print_outfit(outfit)