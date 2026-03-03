from __future__ import annotations

import random
from typing import Optional

import pandas as pd


# Canonical required outfit "slots" (aligned with your item_id prefixes)
REQUIRED_POSITIONS = ["TOP", "BOT", "SHO", "BAG"]
OPTIONAL_POSITIONS_DEFAULT = ["OUT", "LAY", "ACC", "HAT"]


def _normalize_str(x) -> str:
    return str(x).strip().upper()


def _ensure_position_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures a usable 'position' column exists.
    If missing/empty, infer from item_id prefix (TOP_01 -> TOP).
    """
    df = df.copy()

    if "position" not in df.columns:
        df["position"] = ""

    if "item_id" not in df.columns:
        raise KeyError("build_outfit expected column 'item_id' in clothing_df")

    # Fill missing/blank positions from item_id prefix
    pos = df["position"].fillna("").astype(str).str.strip()
    needs_infer = pos.eq("")  # blank positions

    inferred = (
        df.loc[needs_infer, "item_id"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.split("_", n=1)
        .str[0]
    )

    df.loc[needs_infer, "position"] = inferred

    # Normalize all positions to uppercase
    df["position"] = df["position"].apply(_normalize_str)
    POSITION_MAP = {
    "TOP": "TOP",
    "BOTTOM": "BOT",
    "BOT": "BOT",
    "SHOES": "SHO",
    "SHOE": "SHO",
    "SHO": "SHO",
    "BAG": "BAG",
    "OUTER": "OUT",
    "LAYER": "LAY",
    "ACCESSORY": "ACC",
    "HAT": "HAT",
    }
    df["position"] = df["position"].replace(POSITION_MAP)
    return df

def _pick_one(df: pd.DataFrame, position: str, rng: random.Random) -> pd.DataFrame:
    """Pick one row (as 1-row DataFrame) for a given position."""
    pool = df[df["position"] == position]
    if pool.empty:
        raise ValueError(f"No items available for required position: {position}")
    idx = rng.choice(pool.index.tolist())
    return pool.loc[[idx]]


def build_outfit(
    filtered_df: pd.DataFrame,
    temp_celsius: float,
    weather_condition: str,
    *,
    include_optional: bool = True,
    optional_prob: float = 0.5,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """
    Build an outfit from a *filtered* clothing dataframe.

    Expected columns (aligned with data_loader / filters):
        item_id (required)
        position (preferred; inferred from item_id if missing)

    Required positions:
        TOP, BOT, SHO, BAG

    Weather logic:
        - If cold (<= 10°C): require OUT
        - If rainy: require OUT (if any) and prefer SHO items that mention rain
          (If your filtering already enforced weather_condition, this is a light nudge only.)
    """
    if filtered_df is None or len(filtered_df) == 0:
        raise ValueError("build_outfit received an empty filtered_df")

    rng = random.Random(seed)
    df = _ensure_position_column(filtered_df)

    wc = _normalize_str(weather_condition)

    required_positions = list(REQUIRED_POSITIONS)
    optional_positions = list(OPTIONAL_POSITIONS_DEFAULT)

    # --- Temperature logic ---
    if temp_celsius <= 10:
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    # --- Rain logic (align with your standardized weather_condition usage) ---
    if "RAIN" in wc:
        # require outerwear if any exist
        if "OUT" not in required_positions:
            required_positions.append("OUT")

    # --- Build required slots ---
    outfit_parts: list[pd.DataFrame] = []
    for pos in required_positions:
        # If the dataset has no such position at all, fail clearly.
        outfit_parts.append(_pick_one(df, pos, rng))

    # --- Optional slots ---
    if include_optional:
        # Avoid duplicating required positions
        optional_positions = [p for p in optional_positions if p not in required_positions]

        for pos in optional_positions:
            pool = df[df["position"] == pos]
            if pool.empty:
                continue

            if rng.random() < optional_prob:
                idx = rng.choice(pool.index.tolist())
                outfit_parts.append(pool.loc[[idx]])

    outfit_df = pd.concat(outfit_parts, ignore_index=True)

    # Optional: if duplicates happen (same item_id selected twice), drop them.
    if "item_id" in outfit_df.columns:
        outfit_df = outfit_df.drop_duplicates(subset=["item_id"], keep="first").reset_index(drop=True)

    return outfit_df

def print_outfit(outfit_df: pd.DataFrame) -> None:
    if outfit_df is None or outfit_df.empty:
        print("⚠️ Outfit is empty.")
        return

    print("\n✨ GENERATED OUTFIT ✨")
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
    # ⚠️ This block is ONLY for isolated testing.
    # It will NOT run when imported into main.py.

    import pandas as pd

    # Minimal fake test data (aligned with your real structure)
    test_data = pd.DataFrame([
        {"item_id": "TOP_01", "position": "TOP", "category": "T-Shirt", "style": "Casual"},
        {"item_id": "BOT_02", "position": "BOT", "category": "Jeans", "style": "Casual"},
        {"item_id": "SHO_03", "position": "SHO", "category": "Sneakers", "style": "Sporty"},
        {"item_id": "BAG_01", "position": "BAG", "category": "Tote", "style": "Casual"},
        {"item_id": "OUT_01", "position": "OUT", "category": "Jacket", "style": "Casual"},
        {"item_id": "ACC_01", "position": "ACC", "category": "Necklace", "style": "Cute"},
    ])

    outfit = build_outfit(
        filtered_df=test_data,
        temp_celsius=5,
        weather_condition="Rain",
        seed=42
    )

    print_outfit(outfit)

if __name__ == "__main__":
    print("✅ Running outfit_engineer.py directly")

    import pandas as pd

    test_df = pd.DataFrame([
        {"item_id": "TOP_01", "position": "TOP", "category": "T-Shirt", "style": "Casual"},
        {"item_id": "BOT_01", "position": "BOT", "category": "Jeans", "style": "Casual"},
        {"item_id": "SHO_01", "position": "SHO", "category": "Sneakers", "style": "Sporty"},
        {"item_id": "BAG_01", "position": "BAG", "category": "Tote", "style": "Casual"},
        {"item_id": "OUT_01", "position": "OUT", "category": "Jacket", "style": "Casual"},
    ])

    outfit = build_outfit(test_df, temp_celsius=5, weather_condition="Rain", seed=42)
    print_outfit(outfit)
    