import pandas as pd

# Read the CSV file
health_data = pd.read_csv("Data\\healthcare_dataset.csv")

# View the first 5 rows
print(health_data.astype(str))

