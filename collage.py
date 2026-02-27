import os
import pandas as pd
from PIL import Image

# Map your specific categories (from occasion_rules.py) to positions
LAYOUT_MAP = {
    'TOP': {'pos': (200, 100), 'max_size': 350},  # Tops go top-center
    'OUT': {'pos': (450, 100), 'max_size': 400},  # Outerwear/Jackets go top-right
    'BOT': {'pos': (200, 500), 'max_size': 350},  # Bottoms go middle
    'SHO': {'pos': (250, 900), 'max_size': 250},  # Shoes go bottom
    'ACC': {'pos': (50, 50),   'max_size': 200}   # Hats/Bags (Accessories)
}

def load_and_resize(image_path, max_size):
    """Loads a PNG image and resizes it proportionally while keeping transparency."""
    if not os.path.exists(image_path):
        print(f"! Missing image: {image_path}")
        return None
        
    try:
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f"! Error loading {image_path}: {e}")
        return None

def create_collage(outfit_df, output_filename="final_outfit.png"):
    """
    Takes the outfit DataFrame and generates the visual collage.
    Expects outfit_df to have at least: 'item_id' (e.g., 'TOP_02') and 'image_path'.
    """
    # Create blank white canvas
    canvas = Image.new("RGBA", (800, 1200), (255, 255, 255, 255))
    
    # Loop through the final outfit selected by Person 3
    for _, row in outfit_df.iterrows():
        # Look at "TOP_02" and grab just "TOP"
        item_id = str(row.get('item_id', '')).upper()
        prefix = item_id[:3] 
        
        # If it's a known prefix (TOP, BOT, SHO, OUT), get its layout settings
        if prefix in LAYOUT_MAP:
            settings = LAYOUT_MAP[prefix]
        else:
            # Fallback for things like "small bag" or "tie" from your occasion_rules
            settings = LAYOUT_MAP['ACC'] 
            
        img = load_and_resize(row['image_path'], settings['max_size'])
        
        if img:
            # Paste using the image itself as the transparency mask
            canvas.paste(img, settings['pos'], img)

    # Save the file
    canvas.save(output_filename, format="PNG")
    print(f"Outfit collage saved as {output_filename}!")
    return output_filename
