import random
import pandas as pd

def build_outfit(filtered_df, temperature, weather_condition):

    outfit_items = []

    required_types = ["top", "bottoms", "shoes"]
    optional_types = ["accessoires", "bags", "hats", "outerwear"]

    # ---- Temperature logic ----
    if temperature <= 10:
        required_types.append("outerwear")

    if temperature > 25:
        if "outerwear" in optional_types:
            optional_types.remove("outerwear")

    # ---- Rain logic ----
    if weather_condition == "rainy":
        required_types.append("raincoat")
        required_types.append("rainboots")

        # optional: remove normal shoes
        if "shoes" in required_types:
            required_types.remove("shoes")

    # ---- Required categories ----
    for clothing_type in required_types:
        items_of_type = filtered_df[
            filtered_df["type"] == clothing_type
        ]

        if items_of_type.empty:
            print(f"No {clothing_type} available!")
            return None

        selected_item = items_of_type.sample(1)
        outfit_items.append(selected_item)

    # ---- Optional categories ----
    for clothing_type in optional_types:
        items_of_type = filtered_df[
            filtered_df["type"] == clothing_type
        ]

        if not items_of_type.empty:
            if random.random() > 0.5:
                selected_item = items_of_type.sample(1)
                outfit_items.append(selected_item)

    final_outfit = pd.concat(outfit_items, ignore_index=True)

    return final_outfit


weather_df = pd.read_csv("weather.csv")
clothing_df = pd.read_excel("clothing.xlsx")

temperature = 12
weather_condition = "rainy"

filtered_df = clothing_df  # after your filtering steps

outfit = build_outfit(filtered_df, temperature, weather_condition)

print(outfit)
