<h1>📊 Care Transition Efficiency & Outcome Analytics</h1>

A data analytics project to evaluate the efficiency of the CBP → HHS → Sponsor Placement pipeline using Exploratory Data Analysis (EDA) and an interactive Streamlit dashboard
🚀 Project Overview

This project analyzes how efficiently children move through the care system:

CBP Custody (Entry Stage)
Transfer to HHS Care
Discharge to Sponsor (Final Placement)

The analysis focuses on identifying:

Process inefficiencies
System bottlenecks
Backlog accumulation
🎯 Objectives
Measure Transfer Efficiency from CBP to HHS
Evaluate Discharge Effectiveness (placement success)
Detect Backlog and Delays in the system
Build an interactive dashboard for monitoring KPIs
📂 Project Structure
care-transition-project/
│
├── app.py
├── eda.py
├── requirements.txt
├── HHS_Unaccompanied_Alien_Children_Program.csv
├── report/
│   └── Care_Transition_Report.pdf
└── README.md

📊 Key Metrics (KPIs)
| Metric                  | Description                 |
| ----------------------- | --------------------------- |
| Transfer Efficiency     | Speed of CBP → HHS transfer |
| Discharge Effectiveness | Placement success rate      |
| Throughput              | Overall system performance  |
| Backlog                 | Pending/unresolved cases    |

🖥️ Dashboard Features
📅 Date range filtering
📊 KPI summary cards
📈 Time-series visualizations
⚠️ Backlog alerts
📉 Efficiency tracking

🌐 Live Demo
https://hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app/
💡 Key Insights
Backlog occurs when intake exceeds discharge
Transfer efficiency fluctuations indicate process delays
Low discharge effectiveness shows placement bottlenecks
Throughput reflects overall system performance
🛠️ Tech Stack
Python
Pandas
Matplotlib
Streamlit

🔮 Future Improvements
Add predictive model for backlog forecasting
Use interactive visualizations (Plotly)
Improve UI/UX design
Deploy with custom domain
👤 Author

Sahil Gaund
