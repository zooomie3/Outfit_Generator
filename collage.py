from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from PIL import Image


CANVAS_SIZE = (1200, 1600)
CANVAS_BG = (245, 245, 245, 255)

# Pinterest-style free layout
STYLE_LAYOUT = {
    "OUT": {"pos": (640, 120), "max_size": 500, "angle": -4},
    "TOP": {"pos": (650, 980), "max_size": 420, "angle": 2},
    "BOT": {"pos": (700, 620), "max_size": 360, "angle": -2},
    "SHO": {"pos": (140, 620), "max_size": 300, "angle": -8},
    "BAG": {"pos": (80, 80), "max_size": 340, "angle": -3},
    "ACC": {"pos": (160, 360), "max_size": 180, "angle": -10},
    "HAT": {"pos": (260, 1180), "max_size": 260, "angle": 4},
    "LAY": {"pos": (520, 220), "max_size": 300, "angle": 5},
}


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


def _prepare_item_image(img_path: Path, max_size: int, angle: int) -> Image.Image:
    img = Image.open(img_path).convert("RGBA")
    img = _resize_keep_ratio(img, max_size)

    if angle != 0:
        img = img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)

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

    for _, row in outfit_df.iterrows():
        position = str(row["position"]).strip().upper()
        raw_image_path = row["image_path"]

        if pd.isna(raw_image_path):
            print(f"Skipping {position}: image_path is empty")
            continue

        if position not in STYLE_LAYOUT:
            print(f"Skipping unknown position: {position}")
            continue

        img_path = _resolve_image_path(raw_image_path)
        print(f"Trying path for {position}: {img_path}")

        if not img_path.exists():
            print(f"Missing image: {img_path}")
            continue

        try:
            settings = STYLE_LAYOUT[position]
            item_img = _prepare_item_image(
                img_path=img_path,
                max_size=settings["max_size"],
                angle=settings["angle"],
            )
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
