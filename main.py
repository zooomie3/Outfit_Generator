from closet import Closet

closet = Closet("data/closet.csv")
print(closet.get_data().head())

casual_df = closet.filter_for_occasion("casual")
print(casual_df.head())