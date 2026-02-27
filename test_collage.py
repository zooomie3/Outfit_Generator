import os
import pandas as pd
from PIL import Image

# Import YOUR function from your collage.py file
from collage import create_collage

print("🛠️ Setting up test environment...")

# 1. Create a fake 'closet' folder to hold our dummy images
os.makedirs('closet', exist_ok=True)

# 2. Create fake colored squares to act as clothes
Image.new('RGBA', (300, 300), color='red').save('closet/dummy_top.png')
Image.new('RGBA', (300, 300), color='blue').save('closet/dummy_bot.png')
Image.new('RGBA', (200, 200), color='green').save('closet/dummy_sho.png')

# 3. Create a fake outfit DataFrame (This mimics what Person 3 will give you)
fake_outfit_data = pd.DataFrame({
    'item_id': ['TOP_01', 'BOT_01', 'SHO_01'],
    'image_path': ['closet/dummy_top.png', 'closet/dummy_bot.png', 'closet/dummy_sho.png']
})

print("Dummy data ready! Running your collage generator...")

# 4. Run your collage code!
create_collage(fake_outfit_data, "test_output.png")