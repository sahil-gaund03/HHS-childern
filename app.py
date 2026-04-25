# =========================================================
# CARE TRANSITION DASHBOARD (FINAL CLEAN VERSION)
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Care Dashboard", layout="wide")

st.title("📊 Care Transition Efficiency Dashboard")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
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

    # Fix numeric columns
    cols = [
        'cbp_intake',
        'cbp_custody',
        'cbp_transfer',
        'hhs_care',
        'hhs_discharge'
    ]

    for col in cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df[cols] = df[cols].fillna(0)

    return df


df = load_data()

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------
df['transfer_efficiency'] = df['cbp_transfer'] / df['cbp_custody'].replace(0, 1)
df['discharge_effectiveness'] = df['hhs_discharge'] / df['hhs_care'].replace(0, 1)
df['throughput'] = df['hhs_discharge'] / df['cbp_intake'].replace(0, 1)
df['backlog'] = df['cbp_intake'] - df['hhs_discharge']

# Rolling average
df['backlog_ma7'] = df['backlog'].rolling(7).mean()

# ---------------------------------------------------------
# SIDEBAR FILTER
# ---------------------------------------------------------
st.sidebar.header("Filters")

start = st.sidebar.date_input("Start Date", df['date'].min())
end = st.sidebar.date_input("End Date", df['date'].max())

metric_choice = st.sidebar.selectbox(
    "Select Metric",
    ["Transfer Efficiency", "Discharge Effectiveness", "Throughput"]
)

filtered = df[
    (df['date'] >= pd.to_datetime(start)) &
    (df['date'] <= pd.to_datetime(end))
]

# ---------------------------------------------------------
# KPI DISPLAY
# ---------------------------------------------------------
st.subheader("📌 Key Metrics")

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
# ALERT
# ---------------------------------------------------------
if filtered['backlog'].mean() > 0:
    st.warning("⚠️ Backlog present → possible delays")
else:
    st.success("✅ System running smoothly")

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Overview", "⚙️ Efficiency", "📉 Backlog"])

# ---------------- OVERVIEW ----------------
with tab1:
    st.subheader("Pipeline Flow")

    fig, ax = plt.subplots()

    ax.plot(filtered['date'], filtered['cbp_intake'], label="CBP Intake")
    ax.plot(filtered['date'], filtered['hhs_discharge'], label="HHS Discharge")

    # FIX DATE SPACING
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    ax.legend()
    st.pyplot(fig)

# ---------------- EFFICIENCY ----------------
with tab2:
    st.subheader("Efficiency Trend")

    fig, ax = plt.subplots()

    if metric_choice == "Transfer Efficiency":
        ax.plot(filtered['date'], filtered['transfer_efficiency'])
    elif metric_choice == "Discharge Effectiveness":
        ax.plot(filtered['date'], filtered['discharge_effectiveness'])
    else:
        ax.plot(filtered['date'], filtered['throughput'])

    # FIX DATE SPACING
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ---------------- BACKLOG ----------------
with tab3:
    st.subheader("Backlog Trend")

    fig, ax = plt.subplots()

    ax.plot(filtered['date'], filtered['backlog'], label="Backlog")
    ax.plot(filtered['date'], filtered['backlog_ma7'], linestyle='--', label="7-day Avg")

    # FIX DATE SPACING
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    ax.axhline(0)
    ax.legend()

    st.pyplot(fig)

# ---------------------------------------------------------
# INSIGHTS
# ---------------------------------------------------------
st.subheader("📌 Insights")

st.markdown(f"""
- Transfer Efficiency: **{filtered['transfer_efficiency'].mean():.2f}**
- Discharge Effectiveness: **{filtered['discharge_effectiveness'].mean():.2f}**
- Throughput: **{filtered['throughput'].mean():.2f}**
- Average Backlog: **{int(filtered['backlog'].mean())}**

👉 If backlog is consistently positive, system is facing delays.
👉 Improving discharge rate can reduce backlog.
""")

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("View Data"):
    st.dataframe(filtered)
