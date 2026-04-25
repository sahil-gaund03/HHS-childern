import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='UAC Care Analytics', layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv("../data/HHS_Unaccompanied_Alien_Children_Program.csv")

    df.columns = [
        "Date",
        "CBP_Apprehended",
        "CBP_In_Custody",
        "CBP_Transferred",
        "HHS_In_Care",
        "HHS_Discharged"
    ]
    
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df.fillna(method="ffill", inplace=True)
    
    #KPIs
    df["Transfer_Efficiency"] = df["CBP_Transferred"] / df["CBP_In_Custody"]
    df["Discharge_Efficiency"] = df["HHS_Discharged"] / df["HHS_In_Care"]
    df["Throughput"] = df["HHS_Discharged"] / df["CBP_Apprehended"]
    df["Backlog"] = (df["CBP_In_Custody"] + df["HHS_In_Care"]) - df["HHS_Discharged"]
    
    return df

df = load_data()

#sidebar
st.sidebar.title("Filters")
start = st.sidebar.date_input("Start Date", df["Date"].min())
end = st.sidebar.date_input("End Date", df["Date"].max())
    
df = df[(df['Date'] >= pd.to_datetime(start)) & (df['Date']<=pd.to_datetime(end))]

#title
st.title("Care Transition Efficieny Dashboard")

#KPIs
col1, col2, col3, col4  = st.columns(4)

col1.metric("Transfer Efficiency", f"{df['Transfer_Efficiency'].mean():.2f}")
col2.metric("Discharge Efficiency", f"{df['Discharge_Efficiency'].mean():.2f}")
col3.metric("Throughput", f"{df['Throughput'].mean():.2f}")
col4.metric("Max Backlog", int(df["Backlog"].max()))

#flow chart
st.subheader("Pipeline Flow")

fig, ax = plt.subplot()
ax.plot(df['Date'], df['CBP_Apprehended'], label="Apprehended")
ax.plot(df["Date"], df["HHS_Discharged"], label="Discharged")
ax.legend()
st.pyplot(fig)

#efficiency
st.subheader("Efficiency Trends")

fig, ax = plt.subplots()
ax.plot(df["Date"], df["Transfer_Efficiency"], label="Transfer")
ax.plot(df["Date"], df["Discharge_Efficiency"], label="Discharge")
ax.legend()
st.pyplot(fig)

# Backlog
st.subheader("Backlog Analysis")

fig, ax = plt.subplots()
ax.plot(df["Date"], df["Backlog"])
st.pyplot(fig)

# Data
st.subheader("Raw Data")
st.dataframe(df)