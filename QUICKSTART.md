# 🚀 QUICK START GUIDE

## Installation (5 minutes)

### 1. Setup Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Dashboard
```bash
streamlit run app.py
```

✅ Dashboard opens at `http://localhost:8501`

---

## File Structure

```
project/
├── app.py                              # Main entry point
├── pages/
│   ├── 1_🏠_Overview.py               # Page 1: KPIs & Overview
│   ├── 2_🗺️_Global_Analysis.py        # Page 2: Geographic Analysis
│   ├── 3_👤_Athlete_Performance.py    # Page 3: Athlete Stats
│   └── 4_🏟️_Sports_and_Events.py      # Page 4: Events & Venues
├── requirements.txt                    # Dependencies
└── README.md                           # Full documentation
```

---

## Features ✨

✅ **4 Interactive Pages**
- Overview with KPIs
- Geographic analysis with maps
- Athlete performance profiles
- Sports events & venues

✅ **Global Filters**
- Country selection
- Sport selection
- Medal type selection
- Gender filter

✅ **Interactive Charts**
- Pie/Donut charts
- Bar charts
- Choropleth maps
- Sunburst charts
- Treemaps
- Gantt charts
- Scatter maps

✅ **Sample Data Included**
- Works without external files
- 1000+ sample athletes
- 600+ medals
- 500+ events

---

## Customization 🎨

### Add Real Data (Optional)

Download from Kaggle:
https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games

Place CSV files in project root:
- athletes.csv
- medals.csv
- events.csv
- medalists.csv
- schedule.csv
- venues.csv
- nocs.csv

App automatically uses local files if available!

---

## Deployment 🌐

### Streamlit Cloud (Free - Recommended)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Click "New app" → Select repo
4. Share URL with team

### Local Testing
```bash
streamlit run app.py --logger.level=debug
```

### Different Port
```bash
streamlit run app.py --server.port 8502
```

---

## Troubleshooting 🐛

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port 8501 in use | Use `--server.port 8502` |
| Slow loading | Data is cached after first load |
| Charts blank | Try `streamlit cache clear` |

---

## Project Statistics 📊

**Current Capabilities:**
- 👥 1,000+ Athletes
- 🌍 12 Countries
- 🏃 10 Sports
- 🥇 600+ Medals
- 🎯 500+ Events
- 🏟️ 15 Venues

**Technology Stack:**
- Frontend: Streamlit
- Visualization: Plotly
- Data: Pandas, NumPy
- Language: Python 3.8+

---

## Team Assignment Suggestions

**For 3-4 person teams:**

👤 **Person 1: Data Engineer**
- Load and process data
- Create sample data generator
- Handle data transformations

👤 **Person 2: Frontend Developer**
- Build page layouts
- Implement sidebar filters
- Create responsive UI

👤 **Person 3: Visualization Specialist**
- Design interactive charts
- Optimize visualizations
- Choose color schemes

👤 **Person 4 (Optional): QA/DevOps**
- Test all functionality
- Deploy to cloud
- Document processes

---

## Next Steps 📚

1. ✅ Clone/download project
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Run `streamlit run app.py`
4. ✅ Explore all 4 pages
5. ✅ Try all filters
6. ✅ (Optional) Download real data from Kaggle
7. ✅ (Optional) Deploy to Streamlit Cloud

---

## Resources 📖

- Streamlit: https://docs.streamlit.io
- Plotly: https://plotly.com/python/
- Pandas: https://pandas.pydata.org/docs/
- Python: https://python.org

---

## Support 💬

For issues:
1. Check README.md for detailed info
2. Review code comments
3. Check error messages in terminal
4. Try clearing cache: `streamlit cache clear`

---

**Happy Dashboard Building! 🏅**

Created for LA28 Olympic Games Volunteer Selection
Module: Software Engineering For Data Science
Institution: ESI-SBA
