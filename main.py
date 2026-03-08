from __future__ import annotations

from pathlib import Path
from datetime import datetime
import sys

from closet import Closet
from weather import Weather
from outfit_engineer import build_outfit, print_outfit
from collage import create_collage


def _parse_date(date_str: str):
    """
    Accept YYYY-MM-DD or DD-MM-YYYY and return a datetime.date object.
    """
    s = str(date_str).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError("Date format must be YYYY-MM-DD or DD-MM-YYYY")


def _find_first_existing(candidates: list[str | Path]) -> Path:
    """
    Return the first file path that exists from a list of candidates.
    """
    for c in candidates:
        p = Path(c)
        if p.exists():
            return p
    raise FileNotFoundError(
        "Could not find file. Tried: " + ", ".join(str(Path(c)) for c in candidates)
    )


def _prompt(prompt: str, default: str | None = None) -> str:
    """
    Prompt the user for input. If they press enter, use the default value.
    """
    if default:
        text = input(f"{prompt} [{default}]: ").strip()
        return text or default
    return input(f"{prompt}: ").strip()


def main() -> None:
    """
    Run the Fashionista outfit generator.
    """
    print("\nFashionista Outfit Generator")

    date_input = _prompt("Please enter a date", "2026-02-27")
    occasion = _prompt(
        "Please enter an occasion (e.g. casual, gym, beach, night out, family dinner, formal, festival)",
        "casual",
    )

    date_obj = _parse_date(date_input)
    date_str = date_obj.isoformat()

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

    weather = Weather(weather_path)
    closet = Closet(closet_path)

    temp_category = weather.get_temperature_for_date(date_str)
    temp_c, condition = weather.get_weather_for_date(date_str)

    print("\n--- Input Summary ---")
    print("Date:", date_str)
    print("Occasion:", occasion)
    print("Temperature:", f"{temp_c:.1f}°C")
    print("Temperature category:", temp_category)
    print("Weather condition:", condition or "(missing)")

    df = closet.filter_for_occasion(occasion).copy()

    if temp_category:
        df = df[
            df["weather_temp"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.contains(str(temp_category).strip().upper(), regex=False)
        ].copy()

    if condition:
        df = df[
            df["weather_condition"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.contains(str(condition).strip().upper(), regex=False)
        ].copy()

    if df.empty:
        print("\nNo outfit can be generated after filtering.")
        print("Try another date or occasion.")
        return

    outfit_df = build_outfit(
        filtered_df=df,
        temp_celsius=temp_c,
        weather_condition=condition,
        seed=42,
    )

    item_ids = (
        outfit_df["item_id"].astype(str).tolist()
        if "item_id" in outfit_df.columns
        else []
    )

    print("\nSelected item_ids:")
    print(item_ids)

    print_outfit(outfit_df)

    if "image_path" in outfit_df.columns:
        output_file = create_collage(outfit_df, output_filename="final_outfit.png")
        print(f"\nCollage saved as: {output_file}")
    else:
        print("\nNo collage created because there is no 'image_path' column in the final outfit.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nError:", e)
        sys.exit(1)
        