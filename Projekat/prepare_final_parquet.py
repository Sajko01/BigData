import pandas as pd

# ===============================
# 1️⃣ UČITAVANJE CSV FAJLOVA
# ===============================

dem = pd.read_csv("CSV/demographics.csv")
general = pd.read_csv("CSV/general_ema.csv")
covid = pd.read_csv("CSV/covid_ema.csv")
sensing = pd.read_csv("CSV/sensing.csv")
steps = pd.read_csv("CSV/steps.csv")

# ===============================
# 2️⃣ ZADRŽAVAMO BITNE KOLONE
# ===============================

general = general[["uid", "day", "phq4_score", "stress", "social_level"]]
s
covid_cols = ["uid", "day"] + [f"COVID-{i}" for i in range(1, 11)]
covid = covid[covid_cols]

sensing = sensing[["uid", "day", "sleep_duration"]]

# ===============================
# 3️⃣ UKUPNI KORACI
# ===============================

step_cols = [col for col in steps.columns if col.startswith("step_")]
steps["daily_steps"] = steps[step_cols].sum(axis=1)
steps = steps[["uid", "day", "daily_steps"]]

# ===============================
# 4️⃣ UKUPAN COVID SCORE
# ===============================

covid_score_cols = [f"COVID-{i}" for i in range(1, 11)]
covid["covid_total"] = covid[covid_score_cols].sum(axis=1)
covid = covid[["uid", "day", "covid_total"]]

# ===============================
# 5️⃣ SPAJANJE
# ===============================

data = general.merge(sensing, on=["uid", "day"], how="inner")
data = data.merge(steps, on=["uid", "day"], how="inner")
data = data.merge(covid, on=["uid", "day"], how="inner")
data = data.merge(dem, on="uid", how="left")

# ===============================
# 6️⃣ ČIŠĆENJE
# ===============================

data = data.dropna()

print("Final shape:", data.shape)
print(data.head())

# ===============================
# 7️⃣ ČUVANJE U PARQUET
# ===============================

data.to_parquet(
    "college_clean.parquet",
    engine="pyarrow",
    compression="snappy",
    index=False
)

print("Saved as college_clean.parquet")