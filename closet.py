from closet import Closet

from dataset import DataSet
from filters import (
    filter_by_temperature_category,
    filter_by_weather_condition,
    filter_by_occasion
)

class Closet(DataSet):
    def __init__(self, file_path):
        super().__init__(file_path) # file_path inhereted from DataSet parent class

    def show_items(self):
        print(self.get_data())

    def filter_temperature(self, temp_category):
        df = self.get_data()
        return filter_by_temperature_category(df, temp_category)

    def filter_weather(self, weather_condition):
        df = self.get_data()
        return filter_by_weather_condition(df, weather_condition)

    def filter_occasion(self, occasion):
        df = self.get_data()
        return filter_by_occasion(df, occasion)

