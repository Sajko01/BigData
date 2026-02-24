import pandas as pd

# Učitavanje
dem = pd.read_csv("CSV/demographics.csv")
general = pd.read_csv("CSV/general_ema.csv")
covid = pd.read_csv("CSV/covid_ema.csv")
sensing = pd.read_csv("CSV/sensing.csv")
steps = pd.read_csv("CSV/steps.csv")

# ===============================
# 1️⃣ ZADRŽAVAMO SAMO BITNE KOLONE
# ===============================

general = general[["uid", "day", "phq4_score", "stress", "social_level"]]
covid_cols = ["uid", "day"] + [f"COVID-{i}" for i in range(1,11)]
covid = covid[covid_cols]
sensing = sensing[["uid", "day", "sleep_duration"]]

# ===============================
# 2️⃣ PRAVIMO UKUPNE KORAKE
# ===============================

step_cols = [col for col in steps.columns if col.startswith("step_")]
steps["daily_steps"] = steps[step_cols].sum(axis=1)
steps = steps[["uid", "day", "daily_steps"]]

# ===============================
# 3️⃣ PRAVIMO UKUPAN COVID SCORE
# ===============================

covid_score_cols = [f"COVID-{i}" for i in range(1,11)]
covid["covid_total"] = covid[covid_score_cols].sum(axis=1)
covid = covid[["uid", "day", "covid_total"]]

# ===============================
# 4️⃣ SPAJANJE
# ===============================

data = general.merge(sensing, on=["uid","day"], how="inner")
data = data.merge(steps, on=["uid","day"], how="inner")
data = data.merge(covid, on=["uid","day"], how="inner")
data = data.merge(dem, on="uid", how="left")

# ===============================
# 5️⃣ ČIŠĆENJE
# ===============================

data = data.dropna()

print("Final shape:", data.shape)
print(data.head())

# ===============================
# 6️⃣ ČUVANJE
# ===============================

# data.to_parquet("college_clean.parquet")
data.to_csv("college_clean.csv", index=False)