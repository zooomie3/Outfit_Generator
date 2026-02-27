from data_loader import load_weather, load_clothing, get_temperature_for_date, get_weather_for_date

def main():
    print("\n--- Loading Clothing ---")
    clothing_df = load_clothing("data/closet.csv")
    print("Columns:", clothing_df.columns.tolist())
    print(clothing_df.head())

    print("\n--- Loading Weather ---")
    weather_df = load_weather("data/weather.csv")
    print("Columns:", weather_df.columns.tolist())
    print(weather_df.head())

    print("\n--- Temperature Category Test ---")
    temp_category = get_temperature_for_date("2026-02-27", weather_df)
    print("Temp category:", temp_category)

    print("\n--- Full Weather Test ---")
    temp_c, condition = get_weather_for_date("2026-02-27", weather_df)
    print("Temp (C):", temp_c)
    print("Condition:", condition)

if __name__ == "__main__":
    main()

