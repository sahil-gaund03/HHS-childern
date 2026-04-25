import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="UAC Care Analytics", layout="wide")

st.title("Care Transition Efficiency Dashboard")

# ------------------------------
# File Upload
# ------------------------------
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.info("Upload the dataset to begin analysis")
    st.stop()

# ------------------------------
# Load & Clean Data
# ------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # 🔍 Show original columns (debugging)
    st.write("Original Columns:", df.columns.tolist())

    # ------------------------------
    # Rename columns dynamically
    # ------------------------------
    rename_map = {
        "Date": "Date",
        "Children apprehended and placed in CBP custody*": "CBP_Apprehended",
        "Children in CBP custody": "CBP_In_Custody",
        "Children transferred out of CBP custody": "CBP_Transferred",
        "Children in HHS Care": "HHS_In_Care",
        "Children discharged from HHS Care": "HHS_Discharged"
    }

    df = df.rename(columns=rename_map)

    # ------------------------------
    # Ensure required columns exist
    # ------------------------------
    required_cols = [
        "Date",
        "CBP_Apprehended",
        "CBP_In_Custody",
        "CBP_Transferred",
        "HHS_In_Care",
        "HHS_Discharged"
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    # ------------------------------
    # Date handling
    # ------------------------------
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date")

    # ------------------------------
    # Clean numeric columns
    # ------------------------------
    for col in required_cols[1:]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        )

    df.fillna(method="ffill", inplace=True)

    # ------------------------------
    # KPIs
    # ------------------------------
    df["Transfer_Efficiency"] = df["CBP_Transferred"] / df["CBP_In_Custody"].replace(0, np.nan)
    df["Discharge_Efficiency"] = df["HHS_Discharged"] / df["HHS_In_Care"].replace(0, np.nan)
    df["Throughput"] = df["HHS_Discharged"] / df["CBP_Apprehended"].replace(0, np.nan)
    df["Backlog"] = (df["CBP_In_Custody"] + df["HHS_In_Care"]) - df["HHS_Discharged"]

    return df

df = load_data(uploaded_file)
# ------------------------------
# KPIs
# ------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transfer Efficiency", f"{df['Transfer_Efficiency'].mean():.2f}")
col2.metric("Discharge Efficiency", f"{df['Discharge_Efficiency'].mean():.2f}")
col3.metric("Throughput", f"{df['Throughput'].mean():.2f}")
col4.metric("Max Backlog", int(df["Backlog"].max()))

# ------------------------------
# Charts
# ------------------------------
st.subheader("Pipeline Flow")

st.line_chart(df.set_index("Date")[["CBP_Apprehended", "HHS_Discharged"]])

st.subheader("Efficiency Trends")
st.line_chart(df.set_index("Date")[["Transfer_Efficiency", "Discharge_Efficiency"]])

st.subheader("Backlog Trend")
st.line_chart(df.set_index("Date")["Backlog"])

# ------------------------------
# Data Preview
# ------------------------------
st.subheader("Cleaned Dataset")
st.dataframe(df)

