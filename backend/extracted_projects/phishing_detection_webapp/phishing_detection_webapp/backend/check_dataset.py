from scipy.io import arff
import pandas as pd

data, meta = arff.loadarff("dataset.arff")
df = pd.DataFrame(data)

print("Columns:")
print(df.columns)

print("\nLast column name:")
print(df.columns[-1])

print("\nUnique values in last column:")
print(df[df.columns[-1]].unique())
