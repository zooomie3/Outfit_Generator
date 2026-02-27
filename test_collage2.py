import pandas as pd
from collage import create_collage

print("🛠️ Setting up real image test...")

# 1. Update these paths to match exactly what the files are called in your folder!
# For example, if your folder is called 'images' instead of 'closet', change it here.
# Also, make sure the extensions are correct (.png, .jpg, etc.)
real_top = 'Fashionista/tops/TOP_02.png'  
real_bot = 'Fashionista/bottoms/BOT_10.png'
real_sho = 'Fashionista/shoes/SHO_04.png'

# 2. Create the test DataFrame pointing to your real files
real_outfit_data = pd.DataFrame({
    'item_id': ['TOP_02', 'BOT_10', 'SHO_04'],
    'image_path': [real_top, real_bot, real_sho]
})

print("✅ Real data ready! Generating your fashion collage...")

# 3. Run your collage code!
create_collage(real_outfit_data, "real_test_output.png")
