from dataset import DataSet
from closet import Closet
from weather import Weather


print("=== TEST 1: DataSet with closet.csv ===")
dataset = DataSet("data/closet.csv")
print(dataset.get_data().head())
print()

print("=== TEST 2: Closet class ===")
closet = Closet("data/closet.csv")
print("Closet loaded successfully.")
print(closet.get_data().head())
print()

print("=== TEST 3: Closet filter by temperature ===")
print(closet.filter_for_temperature("MILD").head())
print()

print("=== TEST 4: Closet filter by weather ===")
print(closet.filter_for_weather("RAIN").head())
print()

print("=== TEST 5: Closet filter by occasion ===")
print(closet.filter_for_occasion("casual").head())
print()

print("=== TEST 6: Weather class ===")
weather = Weather("data/weather.csv")
print("Weather loaded successfully.")
print(weather.get_data().head())
print()

print("=== TEST 7: Weather temperature category for a date ===")
print(weather.get_temperature_for_date("2025-02-27"))
print()

print("=== TEST 8: Weather details for a date ===")
print(weather.get_weather_for_date("2025-02-27"))
print()