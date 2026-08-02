 # 🇫🇷 Atlantic — France Top 50 Content Compliance Analysis

Audience Sensitivity, Content Compliance & Format Preference Analysis of the France Top 50 Playlist, built for Atlantic Recording Corporation.

## 🔗 Live Dashboard
[View the live Streamlit dashboard](https://atlantic-france-project-prsmcnahd8qfpwst7q8ytn.streamlit.app)

## 📌 Project Overview
This project analyzes 555 days of daily France Top 50 chart snapshots (18-May-2024 to 27-Nov-2025, 27,800 track-days, 325 unique artists) to answer:
- How does explicit content perform relative to clean tracks?
- Do French charts prefer singles or album tracks?
- How does song duration align with listener acceptance?
- Do larger albums dilute or strengthen individual track performance?

## 📁 Project Structure
atlantic-france-project/
├── data/
│ └── Atlantic_France.csv # Raw dataset
├── notebooks/
│ └── eda_analysis.py # Exploratory data analysis script
├── dashboard/
│ └── app.py # Streamlit dashboard
├── outputs/
│ ├── research_paper.md # Full EDA write-up & recommendations
│ └── executive_summary.md # Summary for stakeholders
├── requirements.txt # Python dependencies
└── README.md

## 📊 Key Findings
| KPI | Value |
|---|---|
| Explicit Content Share | 56.3% (62.4% in Top 10) |
| Clean Content Dominance Ratio | 0.78 : 1 |
| Single vs Album Track Ratio | 0.89 : 1 |
| Average Song Duration | 3.09 min |
| Album Size Impact Index | -0.34 |
| Content Acceptance Score (clean, rank-weighted) | 42.6% |

Full details in [`outputs/research_paper.md`](outputs/research_paper.md).

## 🚀 Running Locally

```bash
# Clone the repo
git clone https://github.com/sasanelata05-byte/atlantic-france-project.git
cd atlantic-france-project

# Set up virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
cd dashboard
streamlit run app.py
```

## 🛠️ Tech Stack
- **Python** — pandas, numpy for data processing
- **Streamlit** — interactive dashboard framework
- **Plotly** — data visualizations

## 📄 Deliverables
- ✅ Research paper (EDA, insights, recommendations)
- ✅ Live Streamlit dashboard
- ✅ Executive summary for stakeholders

