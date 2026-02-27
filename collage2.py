import os
import pandas as pd
from PIL import Image

# 1️⃣ Map your specific categories to positions
LAYOUT_MAP = {
    'TOP': {'pos': (200, 100), 'max_size': 350},  
    'OUT': {'pos': (450, 100), 'max_size': 400},  
    'BOT': {'pos': (200, 500), 'max_size': 350},  
    'SHO': {'pos': (250, 900), 'max_size': 250},  
    'ACC': {'pos': (50, 50),   'max_size': 200}   
}

def find_image_in_closet(item_id, closet_folder="closet"):
    """
    Acts as a search engine. Digs through all subfolders in the 'closet' 
    directory to find the image file that matches the item_id.
    """
    item_id = str(item_id).strip().lower()
    
    if not os.path.exists(closet_folder):
        print(f"Error: The folder '{closet_folder}' does not exist here.")
        return None

    # Walk through the closet folder and every subfolder inside it
    for root, dirs, files in os.walk(closet_folder):
        for file in files:
            # Drop the file extension (e.g., '.png') and compare
            file_name_without_ext = file.split('.')[0].lower()
            if file_name_without_ext == item_id:
                # We found it! Combine the folder path and file name
                return os.path.join(root, file)
                
    print(f"Warning: Could not find any image for '{item_id}' in {closet_folder}/")
    return None

def load_and_resize(image_path, max_size):
    """Loads a PNG image and resizes it proportionally while keeping transparency."""
    if not image_path:
        return None
        
    try:
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f" Error loading image at {image_path}: {e}")
        return None

def create_collage(outfit_df, output_filename="final_outfit.png"):
    """
    Takes the outfit DataFrame and generates the visual collage.
    """
    print("Starting collage generation...")
    # Create blank white canvas
    canvas = Image.new("RGBA", (800, 1200), (255, 255, 255, 255))
    
    # Loop through the final outfit selected by Person 3
    for _, row in outfit_df.iterrows():
        # Get the item ID (e.g., 'TOP_02')
        item_id = str(row.get('item_id', '')).upper()
        prefix = item_id[:3] 
        
        # Find exactly where this image is hiding in the subfolders!
        found_image_path = find_image_in_closet(item_id)
        
        # Assign layout settings
        if prefix in LAYOUT_MAP:
            settings = LAYOUT_MAP[prefix]
        else:
            settings = LAYOUT_MAP['ACC'] 
            
        # Load and paste
        img = load_and_resize(found_image_path, settings['max_size'])
        if img:
            # Paste using the image itself as the transparency mask
            canvas.paste(img, settings['pos'], img)
            print(f"  -> Successfully added {item_id} to the canvas.")

    # Save the file
    canvas.save(output_filename, format="PNG")
    print(f"Outfit collage saved as {output_filename}!")
    return output_filename