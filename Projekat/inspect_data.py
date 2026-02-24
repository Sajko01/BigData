import pandas as pd
import os

base_path = "CSV"

files = {
    "demographics": os.path.join(base_path, "demographics.csv"),
    "covid_ema": os.path.join(base_path, "covid_ema.csv"),
    "general_ema": os.path.join(base_path, "general_ema.csv"),
    "sensing": os.path.join(base_path, "sensing.csv"),
    "steps": os.path.join(base_path, "steps.csv")
}

for name, path in files.items():
    print("\n" + "="*60)
    print(f"FILE: {name}")
    print("="*60)
    
    try:
        df = pd.read_csv(path)
        
        print("\nNumber of rows:", len(df))
        print("\nColumns:")
        print(list(df.columns))
        
        print("\nData types:")
        print(df.dtypes)
        
    except Exception as e:
        print("Error loading file:", e)