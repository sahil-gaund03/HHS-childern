Care Transition Efficiency & Outcome Analytics

A data analytics project focused on evaluating the efficiency of the CBP → HHS → Sponsor Placement pipeline using Exploratory Data Analysis (EDA) and an interactive Streamlit dashboard.

🚀 Project Overview

This project analyzes how efficiently children move through the care system:

CBP Custody (Entry Stage)
Transfer to HHS Care
Discharge to Sponsor (Final Placement)

The goal is to identify:

Process inefficiencies
System bottlenecks
Backlog accumulation
🎯 Objectives
Measure Transfer Efficiency from CBP to HHS
Evaluate Discharge Effectiveness (placement success)
Detect Backlog and Delays
Build an interactive dashboard for monitoring
📂 Project Structure
care-transition-project/
│
├── app.py                     # Streamlit dashboard
├── eda.py                     # Data analysis script
├── requirements.txt           # Dependencies
├── HHS_Unaccompanied_Alien_Children_Program.csv
├── report/
│   └── Care_Transition_Report.pdf
└── README.md
📊 Key Metrics (KPIs)
Metric	Description
Transfer Efficiency	Speed of CBP → HHS transfer
Discharge Effectiveness	Placement success rate
Throughput	Overall system performance
Backlog	Pending/unresolved cases
🖥️ Dashboard Features
📅 Date range filtering
📊 KPI summary cards
📈 Time-series visualizations
⚠️ Backlog alerts
📉 Efficiency tracking
▶️ How to Run
1. Install dependencies
pip install -r requirements.txt
2. Run the app
streamlit run app.py
🌐 Live Demo

👉 https://hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app/
📄 Report

A detailed PDF report is included with:

Visual analysis
KPI insights
Business recommendations
💡 Key Insights
Backlog occurs when intake exceeds discharge
Transfer efficiency varies → indicates process delays
Low discharge effectiveness → placement bottleneck
Throughput reflects overall system health
🛠️ Tech Stack
Python
Pandas
Matplotlib
Streamlit
🔮 Future Improvements
Add predictive model for backlog forecasting
Use Plotly for interactive charts
Improve UI/UX design
Deploy with custom domain
👤 Author

Sahil Gaund
