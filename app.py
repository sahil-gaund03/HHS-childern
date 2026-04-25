# ============================================
# CARE TRANSITION DASHBOARD (FINAL WORKING)
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Care Dashboard", layout="wide")

st.title("📊 Care Transition Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

    # Convert Date
    df['Date'] = pd.to_datetime(df['Date'])

    # Rename columns
    df.columns = [
        "date",
        "cbp_intake",
        "cbp_custody",
        "cbp_transfer",
        "hhs_care",
        "hhs_discharge"
    ]

    # -------------------------------
    # FIX DATA TYPES (IMPORTANT)
    # -------------------------------
    cols = [
        'cbp_intake',
        'cbp_custody',
        'cbp_transfer',
        'hhs_care',
        'hhs_discharge'
    ]

    for col in cols:
        # Remove commas (e.g., "1,234")
        df[col] = df[col].astype(str).str.replace(',', '')

        # Convert to numeric
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill only numeric columns
    df[cols] = df[cols].fillna(0)

    return df


df = load_data()

# -------------------------------
# KPI CALCULATIONS (SAFE)
# -------------------------------
df['transfer_efficiency'] = df['cbp_transfer'] / df['cbp_custody'].replace(0, 1)
df['discharge_effectiveness'] = df['hhs_discharge'] / df['hhs_care'].replace(0, 1)
df['backlog'] = df['cbp_intake'] - df['hhs_discharge']

# -------------------------------
# DATE FILTER
# -------------------------------
start = st.date_input("Start Date", df['date'].min())
end = st.date_input("End Date", df['date'].max())

filtered = df[
    (df['date'] >= pd.to_datetime(start)) &
    (df['date'] <= pd.to_datetime(end))
]

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Transfer Efficiency",
            f"{filtered['transfer_efficiency'].mean():.2f}")

col2.metric("Discharge Effectiveness",
            f"{filtered['discharge_effectiveness'].mean():.2f}")

col3.metric("Average Backlog",
            int(filtered['backlog'].mean()))

# -------------------------------
# ALERT
# -------------------------------
if filtered['backlog'].mean() > 0:
    st.warning("⚠️ Backlog detected")
else:
    st.success("✅ System balanced")

# -------------------------------
# PLOTS
# -------------------------------

# Intake vs Discharge
st.subheader("Intake vs Discharge")

fig, ax = plt.subplots()
ax.plot(filtered['date'], filtered['cbp_intake'], label="CBP Intake")
ax.plot(filtered['date'], filtered['hhs_discharge'], label="HHS Discharge")
ax.legend()
st.pyplot(fig)

# Efficiency
st.subheader("Efficiency Trends")

fig, ax = plt.subplots()
ax.plot(filtered['date'], filtered['transfer_efficiency'], label="Transfer Efficiency")
ax.plot(filtered['date'], filtered['discharge_effectiveness'], label="Discharge Effectiveness")
ax.legend()
st.pyplot(fig)

# Backlog
st.subheader("Backlog Trend")

fig, ax = plt.subplots()
ax.plot(filtered['date'], filtered['backlog'])
ax.axhline(0)
st.pyplot(fig)

# -------------------------------
# DATA VIEW
# -------------------------------
st.subheader("Data Preview")
st.dataframe(filtered)
