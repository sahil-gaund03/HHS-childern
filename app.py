# =========================================================
# CARE TRANSITION ANALYTICS DASHBOARD
# Clean • Professional • Intern-Level
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Care Analytics", layout="wide")

# ---------------------------------------------------------
# LOAD DATA (SAFE)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

    # Convert date
    df['Date'] = pd.to_datetime(df['Date'])

    # Rename columns (clean naming)
    df.columns = [
        "date",
        "cbp_intake",
        "cbp_custody",
        "cbp_transfer",
        "hhs_care",
        "hhs_discharge"
    ]

    # Fix numeric columns
    num_cols = [
        'cbp_intake',
        'cbp_custody',
        'cbp_transfer',
        'hhs_care',
        'hhs_discharge'
    ]

    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df[num_cols] = df[num_cols].fillna(0)

    return df


df = load_data()

# ---------------------------------------------------------
# FEATURE ENGINEERING (KPIs)
# ---------------------------------------------------------
df['transfer_efficiency'] = df['cbp_transfer'] / df['cbp_custody'].replace(0, 1)
df['discharge_effectiveness'] = df['hhs_discharge'] / df['hhs_care'].replace(0, 1)
df['throughput'] = df['hhs_discharge'] / df['cbp_intake'].replace(0, 1)
df['backlog'] = df['cbp_intake'] - df['hhs_discharge']

# Rolling average (slightly advanced but easy)
df['backlog_ma7'] = df['backlog'].rolling(7).mean()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filters")

start = st.sidebar.date_input("Start Date", df['date'].min())
end = st.sidebar.date_input("End Date", df['date'].max())

metric_choice = st.sidebar.selectbox(
    "Select Metric",
    ["Transfer Efficiency", "Discharge Effectiveness", "Throughput"]
)

filtered = df[(df['date'] >= pd.to_datetime(start)) &
              (df['date'] <= pd.to_datetime(end))]

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("📊 Care Transition Efficiency Dashboard")

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transfer Efficiency",
            f"{filtered['transfer_efficiency'].mean():.2f}")

col2.metric("Discharge Effectiveness",
            f"{filtered['discharge_effectiveness'].mean():.2f}")

col3.metric("Throughput",
            f"{filtered['throughput'].mean():.2f}")

col4.metric("Avg Backlog",
            int(filtered['backlog'].mean()))

# ---------------------------------------------------------
# ALERT SYSTEM
# ---------------------------------------------------------
if filtered['backlog'].mean() > 0:
    st.warning("⚠️ System backlog present → possible delays in placement")
else:
    st.success("✅ System operating smoothly")

# ---------------------------------------------------------
# TABS (Better UI)
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Overview", "⚙️ Efficiency", "📉 Backlog"])

# ---------------- OVERVIEW ----------------
with tab1:
    st.subheader("Pipeline Flow")

    fig, ax = plt.subplots()
    ax.plot(filtered['date'], filtered['cbp_intake'], label="CBP Intake")
    ax.plot(filtered['date'], filtered['hhs_discharge'], label="HHS Discharge")
    ax.legend()
    st.pyplot(fig)

# ---------------- EFFICIENCY ----------------
with tab2:
    st.subheader("Selected KPI Trend")

    fig, ax = plt.subplots()

    if metric_choice == "Transfer Efficiency":
        ax.plot(filtered['date'], filtered['transfer_efficiency'])
    elif metric_choice == "Discharge Effectiveness":
        ax.plot(filtered['date'], filtered['discharge_effectiveness'])
    else:
        ax.plot(filtered['date'], filtered['throughput'])

    st.pyplot(fig)

# ---------------- BACKLOG ----------------
with tab3:
    st.subheader("Backlog Analysis")

    fig, ax = plt.subplots()
    ax.plot(filtered['date'], filtered['backlog'], label="Backlog")
    ax.plot(filtered['date'], filtered['backlog_ma7'], linestyle='--', label="7-day Avg")
    ax.axhline(0)
    ax.legend()
    st.pyplot(fig)

# ---------------------------------------------------------
# INSIGHTS (IMPORTANT FOR PROJECT)
# ---------------------------------------------------------
st.subheader("📌 Key Insights")

st.markdown(f"""
- Average transfer efficiency is **{filtered['transfer_efficiency'].mean():.2f}**, showing movement speed from CBP to HHS.
- Discharge effectiveness of **{filtered['discharge_effectiveness'].mean():.2f}** reflects placement success.
- A backlog of **{int(filtered['backlog'].mean())}** indicates system pressure.
- Throughput helps evaluate overall pipeline performance.
""")

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("View Data"):
    st.dataframe(filtered)
