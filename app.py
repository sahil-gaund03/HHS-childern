import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="UAC Care Analytics", layout="wide")

# ------------------------------
# Load Data (NO UPLOADER)
# ------------------------------
@st.cache_data
def load_data():
    try:
        # Get current file directory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Build path safely
        file_path = os.path.join(BASE_DIR, "HHS_Unaccompanied_Alien_Children_Program.csv")

        df = pd.read_csv(file_path)

        # Rename columns (your dataset)
        df = df.rename(columns={
            "Children apprehended and placed in CBP custody*": "CBP_Apprehended",
            "Children in CBP custody": "CBP_In_Custody",
            "Children transferred out of CBP custody": "CBP_Transferred",
            "Children in HHS Care": "HHS_In_Care",
            "Children discharged from HHS Care": "HHS_Discharged"
        })

        # Date
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.sort_values("Date")

        # Clean numeric columns
        cols = [
            "CBP_Apprehended",
            "CBP_In_Custody",
            "CBP_Transferred",
            "HHS_In_Care",
            "HHS_Discharged"
        ]

        for col in cols:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "").str.strip(),
                errors="coerce"
            )

        df.fillna(method="ffill", inplace=True)

        # KPIs
        df["Transfer_Efficiency"] = df["CBP_Transferred"] / df["CBP_In_Custody"].replace(0, np.nan)
        df["Discharge_Efficiency"] = df["HHS_Discharged"] / df["HHS_In_Care"].replace(0, np.nan)
        df["Throughput"] = df["HHS_Discharged"] / df["CBP_Apprehended"].replace(0, np.nan)
        df["Backlog"] = (df["CBP_In_Custody"] + df["HHS_In_Care"]) - df["HHS_Discharged"]

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()


df = load_data()
