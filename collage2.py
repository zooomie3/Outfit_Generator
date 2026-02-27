import os
import pandas as pd
from PIL import Image

# This tells the code where to put each type of clothing on the screen
LAYOUT_MAP = {
    'TOP': {'pos': (10, 10), 'max_size': 500},  
    'OUT': {'pos': (350, 200), 'max_size': 530},  
    'BOT': {'pos': (30, 250), 'max_size': 600},  
    'SHO': {'pos': (150, 800), 'max_size': 400},  
    'ACC': {'pos': (450, 500), 'max_size': 500},
    'HAT': {'pos': (500, 0), 'max_size': 500},
    'BAG': {'pos': (500, 600), 'max_size': 400},
    'LAY': {'pos': (200, 100), 'max_size': 500}
}

def find_image(item_id, base_folder="."):
    # Searches your ENTIRE project folder (and all subfolders) to find the image that matches the item_id.
    
    item_id = str(item_id).strip().lower()
    
    # Walk through the current directory ('.') and all its subfolders
    for root, dirs, files in os.walk(base_folder):
        # Skip system folders to speed things up
        if '.git' in root or '__pycache__' in root:
            continue
            
        for file in files:
            # Drop the file extension (e.g., '.png') and compare names
            file_name_without_ext = file.split('.')[0].lower()
            
            if file_name_without_ext == item_id:
                # Found it! Return the exact path
                return os.path.join(root, file)
                
    print(f"⚠️ Warning: Could not find any image for '{item_id}' in your folders.")
    return None

def load_and_resize(image_path, max_size):
    """Safely loads and resizes the image."""
    if not image_path:
        return None
    try:
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f"⚠️ Error loading image at {image_path}: {e}")
        return None

def create_collage(outfit_df, output_filename="final_outfit.png"):
    """Generates the visual collage from the provided DataFrame."""
    print("🎨 Starting collage generation...")
    
    # Create a blank white canvas
    canvas = Image.new("RGBA", (800, 1200), (255, 255, 255, 255))
    
    for _, row in outfit_df.iterrows():
        # Safely grab the item_id from the dataframe
        item_id = str(row.get('item_id', '')).upper()
        
        # If the row is empty or invalid, skip it
        if not item_id or item_id == 'NAN':
            continue
            
        prefix = item_id[:3] # Gets 'TOP', 'BOT', etc.
        
        # 1. Use the search engine to find the image!
        found_image_path = find_image(item_id)
        
        # 2. Get layout settings
        if prefix in LAYOUT_MAP:
            settings = LAYOUT_MAP[prefix]
        else:
            settings = LAYOUT_MAP['ACC'] 
            
        # 3. Load, resize, and paste onto canvas
        img = load_and_resize(found_image_path, settings['max_size'])
        if img:
            canvas.paste(img, settings['pos'], img)
            print(f"  -> Successfully added {item_id} to the canvas.")

    canvas.save(output_filename, format="PNG")
    print(f"✅ Outfit collage saved as {output_filename}!")
    return output_filename
