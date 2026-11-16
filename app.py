import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Hospital Management Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Hospital Management Dashboard")
st.markdown("### Hospital Data Analysis and Bed Occupancy Forecasting")

# SIDEBAR
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Bed Occupancy",
        "ICU Analysis",
        "Patient Analysis",
        "Forecasting",
        "Scenario Analysis",
        "Dataset"
    ]
)

# FILE UPLOAD
uploaded_file = st.sidebar.file_uploader(
    "Upload Hospital Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

else:
    st.info("Please upload your Hospital_Data.xlsx file.")
    st.stop()

# VALIDATE DATA
required_columns = [
    "Date", "Total Beds", "Occupied Beds",
    "ICU Occupied", "ICU Beds",
    "Admissions", "Discharges",
    "Average Length of Stay"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# DATA CLEANING
df = df.drop_duplicates().copy()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df = df.sort_values("Date")

# CALCULATIONS
df["Available Beds"] = (
    df["Total Beds"] - df["Occupied Beds"]
)

df["Bed Occupancy Rate"] = (
    df["Occupied Beds"] /
    df["Total Beds"].replace(0, float("nan"))
) * 100

df["ICU Occupancy Rate"] = (
    df["ICU Occupied"] /
    df["ICU Beds"].replace(0, float("nan"))
) * 100

df["Forecast_Beds"] = (
    df["Occupied Beds"]
    .shift(1)
    .rolling(7)
    .mean()
)

# DASHBOARD
if page == "Dashboard":

    st.subheader("Hospital Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Beds",
        f"{df['Total Beds'].iloc[-1]:,.0f}"
    )

    col2.metric(
        "Occupied Beds",
        f"{df['Occupied Beds'].iloc[-1]:,.0f}"
    )

    col3.metric(
        "Available Beds",
        f"{df['Available Beds'].iloc[-1]:,.0f}"
    )

    col4.metric(
        "Bed Occupancy Rate",
        f"{df['Bed Occupancy Rate'].iloc[-1]:.2f}%"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Admissions",
        int(df["Admissions"].sum())
    )

    col2.metric(
        "Total Discharges",
        int(df["Discharges"].sum())
    )

    col3.metric(
        "Average ICU Occupancy",
        f"{df['ICU Occupancy Rate'].mean():.2f}%"
    )

    st.subheader("Bed Occupancy Trend")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Date"], df["Occupied Beds"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Occupied Beds")
    ax.set_title("Hospital Bed Occupancy Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# BED OCCUPANCY
elif page == "Bed Occupancy":

    st.subheader("Bed Occupancy Analysis")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["Date"],
        df["Occupied Beds"],
        label="Occupied Beds"
    )

    ax.plot(
        df["Date"],
        df["Available Beds"],
        label="Available Beds"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Beds")
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(
        df[[
            "Date",
            "Total Beds",
            "Occupied Beds",
            "Available Beds",
            "Bed Occupancy Rate"
        ]],
        use_container_width=True
    )

# ICU ANALYSIS
elif page == "ICU Analysis":

    st.subheader("ICU Occupancy Analysis")

    st.metric(
        "Average ICU Occupancy",
        f"{df['ICU Occupancy Rate'].mean():.2f}%"
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["Date"],
        df["ICU Occupied"],
        label="ICU Occupied"
    )

    ax.set_title("ICU Occupancy Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("ICU Occupied")
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# PATIENT ANALYSIS
elif page == "Patient Analysis":

    st.subheader("Admissions vs Discharges")

    st.metric(
        "Total Admissions",
        int(df["Admissions"].sum())
    )

    st.metric(
        "Total Discharges",
        int(df["Discharges"].sum())
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["Date"],
        df["Admissions"],
        label="Admissions"
    )

    ax.plot(
        df["Date"],
        df["Discharges"],
        label="Discharges"
    )

    ax.set_title("Admissions vs Discharges")
    ax.set_xlabel("Date")
    ax.set_ylabel("Patients")
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.write(
        "Average Length of Stay:",
        round(df["Average Length of Stay"].mean(), 2)
    )

# FORECASTING
elif page == "Forecasting":

    st.subheader("Bed Occupancy Forecasting")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["Date"],
        df["Occupied Beds"],
        label="Actual"
    )

    ax.plot(
        df["Date"],
        df["Forecast_Beds"],
        label="Forecast"
    )

    ax.set_title("Actual vs Forecasted Bed Occupancy")
    ax.set_xlabel("Date")
    ax.set_ylabel("Beds")
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.write(
        "Latest Forecast:",
        round(df["Forecast_Beds"].iloc[-1], 2)
        if pd.notna(df["Forecast_Beds"].iloc[-1])
        else "Not enough data"
    )

# SCENARIO ANALYSIS
elif page == "Scenario Analysis":

    st.subheader("Hospital Bed Scenario Analysis")

    total_beds = st.number_input(
        "Total Hospital Beds",
        min_value=1,
        value=int(df["Total Beds"].iloc[-1])
    )

    forecast = st.number_input(
        "Expected Occupied Beds",
        min_value=0.0,
        value=float(df["Occupied Beds"].iloc[-1])
    )

    normal = forecast
    increase_10 = forecast * 1.10
    increase_20 = forecast * 1.20

    st.write("### Forecast Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Normal", f"{normal:.2f}")
    col2.metric("10% Increase", f"{increase_10:.2f}")
    col3.metric("20% Increase", f"{increase_20:.2f}")

    st.write("### Capacity Status")

    for name, value in [
        ("Normal", normal),
        ("10% Increase", increase_10),
        ("20% Increase", increase_20)
    ]:
        if value > total_beds:
            st.warning(f"{name}: Capacity exceeded!")
        else:
            st.success(f"{name}: Within hospital capacity.")

# DATASET
elif page == "Dataset":

    st.subheader("Cleaned Hospital Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="Cleaned_Hospital_Data.csv",
        mime="text/csv"
    )

st.sidebar.success("Hospital Dashboard Ready")
