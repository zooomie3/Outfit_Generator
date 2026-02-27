import os
import random
import pandas as pd

# Import the visualizer you already built!
from collage import create_collage

def scan_wardrobe(base_folder="."):
   
    # Scans all folders and subfolders to find every clothing image you have, and sorts them into a dictionary by type.

    wardrobe = {'TOP': [], 'BOT': [], 'SHO': [], 'OUT': [], 'ACC': [], 'HAT': [], 'BAG': [], 'LAY': []}
    
    for root, dirs, files in os.walk(base_folder):
        if '.git' in root or '__pycache__' in root:
            continue
            
        for file in files:
            # Only look at image files
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                prefix = file[:3].upper() # e.g., "TOP"
                item_id = file.split('.')[0].upper() # e.g., "TOP_02"
                
                # If it's a recognized prefix, add it to our virtual wardrobe
                if prefix in wardrobe:
                    wardrobe[prefix].append(item_id)
                    
    return wardrobe

print("Scanning your folders for clothes...")
my_wardrobe = scan_wardrobe()

print(f"Found: {len(my_wardrobe['TOP'])} Tops, {len(my_wardrobe['BOT'])} Bottoms, {len(my_wardrobe['SHO'])} Shoes")

# --- BUILD THE RANDOM OUTFIT ---
random_outfit = []

# 1. Pick a random Top (if we found any)
if my_wardrobe['TOP']:
    random_outfit.append(random.choice(my_wardrobe['TOP']))

# 2. Pick a random Bottom
if my_wardrobe['BOT']:
    random_outfit.append(random.choice(my_wardrobe['BOT']))

# 3. Pick random Shoes
if my_wardrobe['SHO']:
    random_outfit.append(random.choice(my_wardrobe['SHO']))

# 4. (Optional) 50% chance to add Outerwear!
if my_wardrobe['OUT'] and random.choice([True, False]):
    random_outfit.append(random.choice(my_wardrobe['OUT']))

# 5. (Optional) 50% chance to add an Accessory!
if my_wardrobe['ACC'] and random.choice([True, False]):
    random_outfit.append(random.choice(my_wardrobe['ACC']))
    
# 6. (optional) pick a random hat
if my_wardrobe['HAT'] and random.choice([True, False]):
    random_outfit.append(random.choice(my_wardrobe['HAT']))

# 7. (optional) pick a random bag
if my_wardrobe['BAG']:
    random_outfit.append(random.choice(my_wardrobe['BAG']))

# 8. (optional) pick a random layer
if my_wardrobe['LAY'] and random.choice([True, False]):
    random_outfit.append(random.choice(my_wardrobe['LAY']))


# --- GENERATE THE COLLAGE ---
if len(random_outfit) < 3:
    print("⚠️ Warning: Couldn't find enough clothes to make a full outfit. Check your folders!")
else:
    print(f"🎲 Random outfit selected: {random_outfit}")
    
    # Turn our list into the DataFrame that collage.py expects
    outfit_df = pd.DataFrame({'item_id': random_outfit})
    
    # Send it to your collage generator!
    create_collage(outfit_df, "random_outfit_result.png")