# ============================================
# SIMPLE STREAMLIT DASHBOARD
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Care Transition Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")
df['Date'] = pd.to_datetime(df['Date'])

df.columns = [
    "date",
    "cbp_intake",
    "cbp_custody",
    "cbp_transfer",
    "hhs_care",
    "hhs_discharge"
]

# Fix data types
cols = [
    'cbp_intake',
    'cbp_custody',
    'cbp_transfer',
    'hhs_care',
    'hhs_discharge'
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing
df.fillna(0, inplace=True)

# Safe calculations
df['transfer_efficiency'] = df['cbp_transfer'] / df['cbp_custody'].replace(0, 1)
df['discharge_effectiveness'] = df['hhs_discharge'] / df['hhs_care'].replace(0, 1)
df['backlog'] = df['cbp_intake'] - df['hhs_discharge']

# -------------------------------
# DATE FILTER
# -------------------------------
start = st.date_input("Start Date", df['date'].min())
end = st.date_input("End Date", df['date'].max())

filtered = df[(df['date'] >= pd.to_datetime(start)) &
              (df['date'] <= pd.to_datetime(end))]

# -------------------------------
# KPI DISPLAY
# -------------------------------
st.subheader("Key Metrics")

st.write("Transfer Efficiency:", round(filtered['transfer_efficiency'].mean(),2))
st.write("Discharge Effectiveness:", round(filtered['discharge_effectiveness'].mean(),2))
st.write("Average Backlog:", int(filtered['backlog'].mean()))

# -------------------------------
# BACKLOG ALERT
# -------------------------------
if filtered['backlog'].mean() > 0:
    st.warning("Backlog detected!")
else:
    st.success("System is balanced")

# -------------------------------
# PLOTS
# -------------------------------

st.subheader("Intake vs Discharge")

fig, ax = plt.subplots()
ax.plot(filtered['date'], filtered['cbp_intake'], label="CBP Intake")
ax.plot(filtered['date'], filtered['hhs_discharge'], label="HHS Discharge")
ax.legend()
st.pyplot(fig)

st.subheader("Efficiency Trends")

fig, ax = plt.subplots()
ax.plot(filtered['date'], filtered['transfer_efficiency'], label="Transfer Efficiency")
ax.plot(filtered['date'], filtered['discharge_effectiveness'], label="Discharge Effectiveness")
ax.legend()
st.pyplot(fig)

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
