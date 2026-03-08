from closet import Closet
from weather import Weather

closet = Closet("data/closet.csv")
weather = Weather("data/weather.csv")

print("CLOSET DATA:")
closet.show_items()

print("\nWEATHER DATA:")
weather.show_weather()