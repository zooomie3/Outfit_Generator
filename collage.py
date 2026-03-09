from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from PIL import Image


CANVAS_SIZE = (750, 1150)
CANVAS_BG = (245, 245, 245, 255)

# Body-style layout
LAYOUT_MAP = {
    "HAT": {"pos": (285, 20), "max_size": 210},

    "TOP": {"pos": (220, 80), "max_size": 360},
    "LAY": {"pos": (70, 50), "max_size": 380},
    "OUT": {"pos": (420, 120), "max_size": 450},

    "BOT": {"pos": (225, 380), "max_size": 580},
    "SHO": {"pos": (220, 760), "max_size": 220},

    "ACC": {"pos": (85, 575), "max_size": 180},
    "BAG": {"pos": (465, 490), "max_size": 240},
}

# Paste in this order so top stays visible the most
PASTE_ORDER = ["HAT", "OUT", "LAY", "TOP", "BOT", "SHO", "ACC", "BAG"]


def _resolve_image_path(image_path: str) -> Path:
    image_path = str(image_path).strip()
    path = Path(image_path)

    if path.is_absolute():
        return path

    project_dir = Path(__file__).resolve().parent
    return project_dir / path


def _resize_keep_ratio(img: Image.Image, max_size: int) -> Image.Image:
    img = img.copy()
    img.thumbnail((max_size, max_size))
    return img


def _load_item_image(img_path: Path, max_size: int) -> Image.Image:
    img = Image.open(img_path).convert("RGBA")
    img = _resize_keep_ratio(img, max_size)
    return img


def create_collage(
    outfit_df: pd.DataFrame,
    output_filename: str = "final_outfit.png",
) -> Optional[str]:
    required_cols = {"position", "image_path"}
    missing = required_cols - set(outfit_df.columns)
    if missing:
        raise KeyError(f"create_collage is missing required columns: {missing}")

    canvas = Image.new("RGBA", CANVAS_SIZE, CANVAS_BG)
    pasted_any = False

    # Normalize positions first
    outfit_df = outfit_df.copy()
    outfit_df["position"] = outfit_df["position"].astype(str).str.strip().str.upper()

    # Paste items in visual order
    for position in PASTE_ORDER:
        matching_rows = outfit_df[outfit_df["position"] == position]

        if matching_rows.empty:
            continue

        # In case there is more than one item for a position, just take first
        row = matching_rows.iloc[0]
        raw_image_path = row["image_path"]

        if pd.isna(raw_image_path):
            print(f"Skipping {position}: image_path is empty")
            continue

        if position not in LAYOUT_MAP:
            print(f"Skipping unknown position: {position}")
            continue

        img_path = _resolve_image_path(raw_image_path)
        print(f"Trying path for {position}: {img_path}")

        if not img_path.exists():
            print(f"Missing image: {img_path}")
            continue

        try:
            settings = LAYOUT_MAP[position]
            item_img = _load_item_image(img_path, settings["max_size"])
        except Exception as e:
            print(f"Could not open image {img_path}: {e}")
            continue

        x, y = settings["pos"]
        canvas.paste(item_img, (x, y), item_img)
        pasted_any = True

    if not pasted_any:
        print("No images were pasted onto the canvas.")
        return None

    output_path = Path(__file__).resolve().parent / output_filename
    canvas.save(output_path)
    return str(output_path)
