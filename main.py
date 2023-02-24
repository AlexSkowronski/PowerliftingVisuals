from assets.extract import extract_dataset
import pandas as pd

ADDRESS = "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"

df = pd.read_csv(extract_dataset(ADDRESS))

print(df)