import os
import pandas as pd
from PIL import Image

# Mapping of each clothing category to a specific position and determining its max size on the collage canvas
LAYOUT_MAP = {
    'TOP': {'pos': (200, 100), 'max_size': 350}, 
    'OUT': {'pos': (450, 100), 'max_size': 400}, 
    'BOT': {'pos': (200, 500), 'max_size': 350}, 
    'SHO': {'pos': (250, 900), 'max_size': 250}, 
    'ACC': {'pos': (50, 50),   'max_size': 200}   
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
    Creates a collage of a selected outfit based on the provided DataFrame of clothing items. 
    Expects outfit_df to have at least: 'item_id' (e.g., 'TOP_02') and 'image_path'.
    """
    # Creating a blank white canvas for the collage
    canvas = Image.new("RGBA", (800, 1200), (255, 255, 255, 255))
    
    for _, row in outfit_df.iterrows():
        # Grabs just the category (prefix) of a clothing item (e.g, "TOP" from "TOP_02") to be able to determine where to place it on the canvas 
        item_id = str(row.get('item_id', '')).upper()
        prefix = item_id[:3] 
        
        # If the category is one of the following: TOP, BOT, SHO, OUT, get its layout settings
        if prefix in LAYOUT_MAP:
            settings = LAYOUT_MAP[prefix]
        else:
            # If something else, means it's likely an accessory 
            settings = LAYOUT_MAP['ACC'] 
            
        img = load_and_resize(row['image_path'], settings['max_size'])
        
        if img:
        
            canvas.paste(img, settings['pos'], img)

    # Saving the file  
    canvas.save(output_filename, format="PNG")
    print(f"Outfit collage saved as {output_filename}!")
    return output_filename
