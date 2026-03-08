import os
from PIL import Image

LAYOUT_MAP = {
    "TOP": {"pos": (200, 100), "max_size": 350},
    "OUT": {"pos": (450, 100), "max_size": 400},
    "LAY": {"pos": (450, 250), "max_size": 350},
    "BOT": {"pos": (200, 500), "max_size": 350},
    "SHO": {"pos": (250, 900), "max_size": 250},
    "BAG": {"pos": (520, 650), "max_size": 220},
    "ACC": {"pos": (50, 50), "max_size": 180},
    "HAT": {"pos": (80, 20), "max_size": 180},
}


def load_and_resize(image_path, max_size):
    """
    Load an image and resize it proportionally while keeping transparency.

    Parameters:
        image_path (str): Path to the clothing item image.
        max_size (int): Maximum width/height for the resized image.

    Returns:
        PIL.Image.Image or None: The resized image, or None if loading fails.
    """
    if not os.path.exists(image_path):
        print(f"Missing image: {image_path}")
        return None

    try:
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None


def create_collage(outfit_df, output_filename="final_outfit.png"):
    """
    Create a collage from the selected outfit items.

    The function expects the outfit DataFrame to contain:
    - item_id
    - image_path

    The first three letters of item_id are used to decide where each image
    should be placed on the canvas.

    Parameters:
        outfit_df (pandas.DataFrame): DataFrame containing the selected outfit items.
        output_filename (str): Name of the PNG file to save.

    Returns:
        str: The filename of the saved collage image.
    """
    canvas = Image.new("RGBA", (800, 1200), (255, 255, 255, 255))

    for _, row in outfit_df.iterrows():
        item_id = str(row.get("item_id", "")).upper()
        prefix = item_id[:3]

        if prefix in LAYOUT_MAP:
            settings = LAYOUT_MAP[prefix]
        else:
            settings = LAYOUT_MAP["ACC"]

        img = load_and_resize(row["image_path"], settings["max_size"])

        if img:
            canvas.paste(img, settings["pos"], img)

    canvas.save(output_filename, format="PNG")
    print(f"Outfit collage saved as {output_filename}!")
    return output_filename

