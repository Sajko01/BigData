import pandas as pd
import os

df = pd.read_csv("college_clean.csv")

# koliko puta da ponovimo
multiplier = 1500   # 

big_df = pd.concat([df] * multiplier, ignore_index=True)

print("Original rows:", len(df))
print("New rows:", len(big_df))

big_df.to_csv("college_big.csv", index=False)