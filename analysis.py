import pandas as pd

file = "Hospital_Data.xlsx"

df = pd.read_excel(file)

print(df.head())

print("Missing Values:")
print(df.isnull().sum())


print("Duplicate Rows:")
print(df.duplicated().sum())


df = df.drop_duplicates()


df["Date"] = pd.to_datetime(df["Date"])


df = df.sort_values("Date")

print("Data cleaning completed.")

df["Available Beds"] = (
    df["Total Beds"] - df["Occupied Beds"]
)
df["Bed Occupancy Rate"] = (
    df["Occupied Beds"] /
    df["Total Beds"]
) * 100
df["ICU Occupancy Rate"] = (
    df["ICU Occupied"] /
    df["ICU Beds"]
) * 100

print("Average Bed Occupancy:",
      df["Bed Occupancy Rate"].mean())

print("Average ICU Occupancy:",
      df["ICU Occupancy Rate"].mean())

print("Average Available Beds:",
      df["Available Beds"].mean())

print("Total Admissions:",
      df["Admissions"].sum())

print("Total Discharges:",
      df["Discharges"].sum())

print("Average Length of Stay:",
      df["Average Length of Stay"].mean())

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

plt.plot(
    df["Date"],
    df["Occupied Beds"]
)

plt.xlabel("Date")
plt.ylabel("Occupied Beds")
plt.title("Hospital Bed Occupancy Trend")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

plt.figure(figsize=(10,5))

plt.plot(
    df["Date"],
    df["ICU Occupied"]
)

plt.xlabel("Date")
plt.ylabel("ICU Occupied")
plt.title("ICU Occupancy Trend")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

plt.figure(figsize=(10,5))

plt.plot(
    df["Date"],
    df["Admissions"],
    label="Admissions"
)

plt.plot(
    df["Date"],
    df["Discharges"],
    label="Discharges"
)

plt.xlabel("Date")
plt.ylabel("Number of Patients")
plt.title("Admissions vs Discharges")

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

df.to_csv(
    "Cleaned_Hospital_Data.csv",
    index=False
)

print("Cleaned dataset saved.")

df["Forecast_Beds"] = (
    df["Occupied Beds"]
    .shift(1)
    .rolling(7)
    .mean()
)

plt.figure(figsize=(10,5))

plt.plot(
    df["Date"],
    df["Occupied Beds"],
    label="Actual"
)

plt.plot(
    df["Date"],
    df["Forecast_Beds"],
    label="Forecast"
)

plt.xlabel("Date")
plt.ylabel("Beds")
plt.title("Actual vs Forecasted Bed Occupancy")

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

forecast = 88
total_beds = 100

normal = forecast
increase_10 = forecast * 1.10
increase_20 = forecast * 1.20

print("Normal:", normal)
print("10% Increase:", increase_10)
print("20% Increase:", increase_20)