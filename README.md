<div align="center">

# 📊 Care Transition Efficiency & Outcome Analytics

### Government Data Analytics · Pipeline Monitoring · Real-Time Streamlit Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557c?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app/)

<br/>

> **Measure, monitor, and surface inefficiencies in the CBP → HHS → Sponsor Placement pipeline.**  
> A government data analytics project built on 1,170 daily records spanning January 2023 – December 2025, with four real-time KPIs, time-series visualizations, backlog trend tracking, and a fully interactive Streamlit dashboard.

<br/>

[![Live Demo](https://img.shields.io/badge/▶_Open_Live_Dashboard-hhs--childern.streamlit.app-FF4B4B?style=flat-square&logo=streamlit)](https://hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app/)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Pipeline Architecture](#-pipeline-architecture)
- [Business KPIs](#-business-kpis)
- [Dataset](#-dataset)
- [Key Insights](#-key-insights)
- [Folder Structure](#-folder-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Deployment](#-deployment)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🧠 Overview

The HHS Unaccompanied Children Program moves children through a three-stage system:

```
CBP Custody (Entry)  →  HHS Care (Processing)  →  Sponsor Placement (Exit)
```

Delays at any stage accumulate as backlog — a policy-critical problem that is difficult to detect without real-time monitoring.

This project applies exploratory data analysis and KPI engineering to **720 records of daily government data** (Jan 2023 – Dec 2025), then surfaces those insights through an interactive Streamlit dashboard filterable by any date range.

**What this project delivers:**

- 📐 Four derived KPIs computed from raw intake and discharge counts
- 📈 Time-series trend analysis with 7-day moving averages on backlog
- ⚠️ Backlog detection: flags when intake outpaces discharge
- 🖥️ A date-filtered Streamlit dashboard with live metric recalculation

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Data Processing** | Pandas, NumPy | Data cleaning, KPI derivation, rolling averages |
| **Visualization** | Matplotlib, Seaborn | Time-series charts, efficiency trend plots |
| **Dashboard** | Streamlit | Interactive UI with sidebar filters and KPI cards |
| **Date Handling** | Matplotlib Dates | Quarterly date axis formatting for readability |
| **Deployment** | Streamlit Community Cloud | Live hosting |

---

## ✨ Features

<details>
<summary><strong>🔹 KPI Engineering</strong></summary>

Five metrics derived from raw CBP and HHS columns to quantify pipeline performance:

| KPI | Formula | Interpretation |
|---|---|---|
| `transfer_efficiency` | `cbp_transfer / cbp_custody` | How quickly children move from CBP to HHS |
| `discharge_effectiveness` | `hhs_discharge / hhs_care` | Placement success rate out of HHS care |
| `throughput` | `hhs_discharge / cbp_intake` | End-to-end system output relative to intake |
| `backlog` | `cbp_intake − hhs_discharge` | Daily surplus of intake over discharge |
| `backlog_ma7` | 7-day rolling mean of backlog | Smoothed backlog trend for signal clarity |

</details>

<details>
<summary><strong>🔹 Interactive Streamlit Dashboard</strong></summary>

| Section | Description |
|---|---|
| **KPI Cards** | Transfer Efficiency · Discharge Effectiveness · Throughput · Avg Backlog — all recalculate on date filter |
| **Pipeline Flow Chart** | Daily CBP Intake vs. HHS Discharge plotted on one axis to show the gap visually |
| **Backlog Trend** | Raw backlog line + 7-day moving average; zero line marks the tipping point |
| **Efficiency Trends** | Transfer efficiency and discharge effectiveness over time on a shared axis |
| **Key Insights Panel** | Auto-computed summary of current filter's averages with interpretation |
| **Raw Data Expander** | Full filtered dataset in an expandable table |

</details>

<details>
<summary><strong>🔹 Data Cleaning Pipeline</strong></summary>

The raw CSV contains comma-formatted numbers and mixed date strings. The load pipeline handles:

- Parsing `"December 21, 2025"` format dates with `pd.to_datetime`
- Stripping commas from numeric strings (`"2,484"` → `2484`)
- Coercing non-numeric entries to `NaN` then filling with `0`
- Renaming six raw columns to clean, snake_case names
- Division-by-zero protection on all KPI calculations via `.replace(0, 1)`

</details>

---

## 🏗 Pipeline Architecture

```
HHS_Unaccompanied_Alien_Children_Program.csv
              │
              ▼
┌─────────────────────────────┐
│       Data Cleaning         │
│  • Parse dates              │
│  • Strip comma formatting   │
│  • Coerce to numeric        │
│  • Fill NaN → 0             │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│       KPI Engineering       │
│  • Transfer Efficiency      │
│  • Discharge Effectiveness  │
│  • Throughput               │
│  • Backlog + 7-day MA       │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│    Streamlit Dashboard      │
│  • Date range sidebar       │
│  • Live KPI cards           │
│  • 3 chart panels           │
│  • Insights + raw data      │
└─────────────────────────────┘
```

---

## 📈 Business KPIs

All four KPIs are computed from the filtered date range and displayed as Streamlit metric cards:

| KPI | Avg Value (Full Dataset) | Alert Condition |
|---|---|---|
| **Transfer Efficiency** | 0.69 | < 0.5 signals CBP bottleneck |
| **Discharge Effectiveness** | 0.02 | Low ratio → placement capacity constrained |
| **Throughput** | 2.54 | < 1.0 means system output lags intake |
| **Avg Backlog** | −79 | Positive backlog → accumulating delays |

> Values computed from 720 daily records across January 2023 – December 2025. Peak HHS care census reached **11,516 children**.

---

## 🗂 Dataset

| Property | Value |
|---|---|
| **File** | `HHS_Unaccompanied_Alien_Children_Program.csv` |
| **Source** | HHS / CBP government program data |
| **Records** | 1,170 rows (720 with complete numeric data) |
| **Date Range** | January 12, 2023 – December 21, 2025 |
| **Frequency** | Daily |
| **Columns** | 6 (date + 5 numeric pipeline metrics) |

**Column reference after cleaning:**

| Raw Column | Cleaned Name | Description |
|---|---|---|
| Date | `date` | Daily record date |
| Children apprehended and placed in CBP custody | `cbp_intake` | Daily new arrivals entering CBP |
| Children in CBP custody | `cbp_custody` | Current CBP holding count |
| Children transferred out of CBP custody | `cbp_transfer` | Daily transfers from CBP to HHS |
| Children in HHS Care | `hhs_care` | Current HHS care population |
| Children discharged from HHS Care | `hhs_discharge` | Daily placements to sponsors |

---

## 💡 Key Insights

| Finding | Detail |
|---|---|
| 🔴 **Backlog occurs when intake exceeds discharge** | Visible in the Pipeline Flow chart as the gap between intake and discharge lines widens |
| 📉 **Transfer efficiency fluctuations signal process delays** | Sharp drops in `transfer_efficiency` correlate with custody surges at CBP |
| ⚠️ **Low discharge effectiveness = placement bottleneck** | The 0.02 average reflects HHS care capacity pressure relative to the children in care |
| 📊 **Throughput above 1.0 indicates drawdown periods** | When discharge exceeds intake, backlog is being resolved — visible in the 7-day MA trend |
| 🏔️ **Peak HHS care census hit 11,516 children** | The highest recorded `hhs_care` value, indicating maximum system load in the dataset |

---

## 📁 Folder Structure

```
HHS-childern-main/
│
├── app.py                                         # Streamlit dashboard — main entry point
├── Untitled.ipynb                                 # EDA notebook — cleaning, KPIs, charts
├── HHS_Unaccompanied_Alien_Children_Program.csv   # Source dataset (daily, 2023–2025)
├── requirements.txt                               # Python dependencies
└── README.md                                      # You are here
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/sahil-gaund03/HHS-childern.git
cd HHS-childern

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

The dashboard opens at `http://localhost:8501` by default.

---

## 🚀 Usage

### Running the Dashboard

```bash
streamlit run app.py
```

**Sidebar controls:**
- **Start / End date** — filters all KPI cards and charts to the selected range
- All four KPIs recalculate automatically on filter change

**Reading the charts:**

| Chart | How to read it |
|---|---|
| Pipeline Flow | Gap between Intake and Discharge lines = active backlog |
| Backlog Trend | Positive values = intake outpacing discharge; dashed line = 7-day smoothed average |
| Efficiency Trends | Both lines ideally stay above 0.5; sustained drops indicate system stress |

### Running the Notebook

```bash
jupyter notebook Untitled.ipynb
```

Covers the full EDA workflow: data loading → cleaning → KPI derivation → visualization.

---

## 🖼 Screenshots

> _Add screenshots to a `/screenshots` folder and update the paths below._

| View | Description |
|---|---|
| ![KPI Cards](https://via.placeholder.com/800x200?text=KPI+Cards+%E2%80%94+Transfer+Efficiency+%C2%B7+Discharge+%C2%B7+Throughput+%C2%B7+Backlog) | Four live KPI metrics with date-filtered values |
| ![Pipeline Flow](https://via.placeholder.com/800x350?text=Pipeline+Flow+Chart+%E2%80%94+Intake+vs+Discharge) | Daily CBP intake vs. HHS discharge time series |
| ![Backlog Trend](https://via.placeholder.com/800x350?text=Backlog+Trend+%E2%80%94+Raw+%2B+7-Day+MA) | Backlog with 7-day moving average overlay |
| ![Efficiency Trends](https://via.placeholder.com/800x350?text=Efficiency+Trends+%E2%80%94+Transfer+%26+Discharge) | Transfer and discharge efficiency over time |
| ![Raw Data](https://via.placeholder.com/800x300?text=Expandable+Raw+Data+Table) | Filterable raw dataset expander |

---

## ☁️ Deployment

### Streamlit Cloud (Current)

The app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push repository to GitHub (ensure `app.py` and the CSV are both in the root)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

🔗 **Live:** [hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app](https://hhs-childern-mrngtcx3tgawjkzzcju6h2.streamlit.app/)

---

<details>
<summary><strong>Docker (Optional)</strong></summary>

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t hhs-care-dashboard .
docker run -p 8501:8501 hhs-care-dashboard
```

</details>

---

## 🔮 Future Improvements

| Area | Planned Enhancement |
|---|---|
| **Forecasting** | Predictive backlog model using ARIMA or Facebook Prophet |
| **Visualization** | Migrate charts to Plotly for interactive hover, zoom, and pan |
| **Alerts** | Threshold-based alerts when backlog exceeds configurable limits |
| **Annotations** | Tie chart events to known policy changes for contextual analysis |
| **UI/UX** | Custom Streamlit theme and layout refinements |
| **Deployment** | Custom domain with CI/CD pipeline on Render or Railway |
| **Data Refresh** | Automated pipeline pulling from public HHS data endpoints |

---

## 🤝 Contributing

Contributions are welcome. To contribute:

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Commit with a clear message
git commit -m "feat: add Plotly interactive charts to dashboard"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

**Before submitting a PR:**
- Confirm the dashboard runs without error (`streamlit run app.py`)
- Keep column names consistent with the cleaned schema (`cbp_intake`, `hhs_care`, etc.)
- Include a brief description of the change in your PR body

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

<div align="center">

**Sahil Gaund**

*Data Science · Analytics Engineering · Government Data*

[![GitHub](https://img.shields.io/badge/GitHub-sahil--gaund03-181717?style=for-the-badge&logo=github)](https://github.com/sahil-gaund03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sahilgaund03-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sahilgaund03)
[![Portfolio](https://img.shields.io/badge/Portfolio-sahilgaund0310.netlify.app-00C7B7?style=for-the-badge&logo=netlify)](https://sahilgaund0310.netlify.app/)

</div>

---

## ⭐ Support

If this project helped you or you found it useful:

- **Star the repo** — it helps others discover the project
- **Fork it** — extend the analysis or adapt it to similar government datasets
- **Share it** — with anyone working in data analytics, policy, or public sector tech

```
⭐ Star this repo if it was useful to you!
```

<div align="center">

---

*Built with Python · Pandas · Matplotlib · Streamlit*

</div>
