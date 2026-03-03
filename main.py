# asks the user for date + occasion
# loads weather.csv + closet.csv
# filters by occasion + temp category + weather condition
# builds an outfit
# prints a list of item_ids + a nicer breakdown

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import sys

import pandas as pd

from data_loader import (
    load_weather,
    load_clothing,
    get_temperature_for_date,
    get_weather_for_date,
)
from filters import (
    filter_by_occasion,
    filter_by_temperature_category,
    filter_by_weather_condition
)
from occasion_rules import OCCASION_RULES
from outfit_engineer import build_outfit, print_outfit


def _parse_date(date_str: str):
    """Accept YYYY-MM-DD or DD-MM-YYYY. Returns datetime.date."""
    s = str(date_str).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError("Date format must be YYYY-MM-DD (recommended) or DD-MM-YYYY")


def _find_first_existing(candidates: list[str | Path]) -> Path:
    for c in candidates:
        p = Path(c)
        if p.exists():
            return p
    raise FileNotFoundError(
        "Could not find file. Tried: " + ", ".join(str(Path(c)) for c in candidates)
    )


def _prompt(prompt: str, default: str | None = None) -> str:
    if default:
        text = input(f"{prompt} [{default}]: ").strip()
        return text or default
    return input(f"{prompt}: ").strip()


def main() -> None:
    print("\n🧥 Fashionista Outfit Generator")

    # ---- 1) User input ----
    date_input = _prompt("Enter a date", "year-month-day")
    occasion = _prompt(
        "Enter an occasion (e.g., casual, gym, beach, night out, family dinner, formal, festival)",
        "casual",
    )

    date_obj = _parse_date(date_input)
    date_str = date_obj.isoformat()  # aligns with get_weather_for_date/get_temperature_for_date

    # ---- 2) Locate CSVs (works across common folder layouts) ----
    weather_path = _find_first_existing(
        [
            "Fashionista/weather.csv",
            "data/weather.csv",
            "weather.csv",
            "Weather.csv",
        ]
    )
    closet_path = _find_first_existing(
        [
            "Fashionista/closet.csv",
            "data/closet.csv",
            "closet.csv",
            "Closet.csv",
        ]
    )

    # ---- 3) Load data ----
    weather_df = load_weather(weather_path)
    clothing_df = load_clothing(closet_path)

    # ---- 4) Get weather for date ----
    temp_category = get_temperature_for_date(date_str, weather_df)
    temp_c, condition = get_weather_for_date(date_str, weather_df)

    print("\n📅 Date:", date_str)
    print("🌡️  Temp:", f"{temp_c:.1f}°C", f"({temp_category})")
    print("☁️  Condition:", condition or "(missing)")
    print("🎯 Occasion:", occasion)

    # ---- 5) Apply filters ----
    df = clothing_df

    # Occasion filter (uses OCCASION_RULES item_id allow-list)
    df = filter_by_occasion(df, occasion, OCCASION_RULES)

    # Temperature filter (uses clothing_df['weather_temp'] contains COLD/MILD/WARM/HOT)
    df = filter_by_temperature_category(df, temp_category)

    # Weather condition filter (uses clothing_df['weather_condition'] contains condition)
    # If your closet rows use broader labels (e.g. "RAIN" / "CLEAR"),
    # make sure your weather.csv 'condition' column uses the same style.
    if condition:
        df = filter_by_weather_condition(df, condition)

    if df.empty:
        print("\n⚠️ No items left after filtering.")
        print("Try a different date/occasion, or broaden closet weather_temp/weather_condition values.")
        return

    # ---- 6) Build outfit ----
    outfit_df = build_outfit(
        filtered_df=df,
        temp_celsius=temp_c,
        weather_condition=condition,
        seed=42,  # deterministic results for debugging; remove/change for randomness
    )

    # ---- 7) Output: list of item_ids ----
    item_ids = outfit_df["item_id"].astype(str).tolist() if "item_id" in outfit_df.columns else []

    print("\n✅ Selected item_ids:")
    print(item_ids)

    # Optional pretty print
    print_outfit(outfit_df)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n❌ Error:", e)
        sys.exit(1)

        

