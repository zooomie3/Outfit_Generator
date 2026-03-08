from dataset import DataSet


class Closet(DataSet):
    def __init__(self, file_path):
        super().__init__(file_path) # file_path inhereted from DataSet parent class

    def show_items(self):
        print(self.get_data())

from closet import Closet

