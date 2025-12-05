# 🏅 LA28 Olympic Games Streamlit Dashboard

## 📊 Project Overview

A comprehensive, multi-page Streamlit dashboard for the LA28 Volunteer Selection Committee to analyze Paris 2024 Olympic Games data. This application showcases interactive data visualizations, real-time filtering, and insightful analytics about athletes, medals, sports, venues, and global statistics.

---

## ✨ Features

### 🏠 **Page 1: Overview**
- **KPI Metrics**: Total Athletes, Countries, Sports, Medals, Events
- **Medal Distribution**: Interactive pie/donut chart
- **Top 10 Medal Standings**: Bar chart visualization
- **Medal Breakdown Statistics**: Detailed tables by country

### 🗺️ **Page 2: Global Analysis**
- **World Medal Map**: Choropleth visualization
- **Continental Medal Hierarchy**: Interactive sunburst chart
- **Continent vs Medals**: Bar chart analysis
- **Country Medal Rankings**: Top performers globally

### 👤 **Page 3: Athlete Performance**
- **Athlete Profile Search**: Detailed individual athlete cards
- **Age Distribution**: Box plots by gender
- **Gender Distribution**: Pie charts
- **Top Athletes**: Medal winners ranking
- **Physical Characteristics**: Height and weight distributions

### 🏟️ **Page 4: Sports & Events**
- **Event Schedule**: Gantt chart visualization
- **Medal Count by Sport**: Interactive treemap
- **Venue Locations**: Geographic scatter map
- **Venue Information**: Capacity and location details

### 🎛️ **Global Sidebar Filters**
- 🌍 **Country Selection**: Multiselect for countries
- 🏃 **Sport Selection**: Multiselect for sports
- 🥇 **Medal Types**: Checkboxes for Gold/Silver/Bronze
- 👥 **Gender Filter**: Male/Female selection

---

## 📋 Project Structure

```
streamlit-olympic-dashboard/
│
├── app.py                                    # Main application file
│
├── pages/
│   ├── 1_🏠_Overview.py                     # Overview & KPIs
│   ├── 2_🗺️_Global_Analysis.py              # Geographic insights
│   ├── 3_👤_Athlete_Performance.py          # Athlete statistics
│   └── 4_🏟️_Sports_and_Events.py            # Events & venues
│
├── requirements.txt                          # Python dependencies
│
└── README.md                                 # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Git (optional)

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd streamlit-olympic-dashboard
```

### Step 2: Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Data (Optional)

If you want to use real data from Kaggle:

1. Download from: https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games
2. Extract CSV files to the project directory
3. The app will automatically use local CSV files if available

### Step 5: Run the Application

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ^1.28.0 | Web framework |
| pandas | ^2.0.0 | Data manipulation |
| numpy | ^1.24.0 | Numerical computing |
| plotly | ^5.14.0 | Interactive visualizations |

**See `requirements.txt` for complete list**

---

## 📊 Dataset Files (Optional Local Use)

If using Kaggle dataset, place these CSV files in project root:

| File | Rows | Columns |
|------|------|---------|
| `athletes.csv` | 1,000+ | athlete_id, name, country, sport, age, gender, height_cm, weight_kg |
| `medals.csv` | 600+ | medal_id, athlete_id, country, sport, medal_type, event |
| `events.csv` | 500+ | event_id, event_name, sport, date, venue |
| `medalists.csv` | 600+ | athlete info + medal details |
| `schedule.csv` | 500+ | event_id, sport, date, venue |
| `venues.csv` | 15+ | venue_id, venue_name, capacity, latitude, longitude |
| `nocs.csv` | 100+ | country, continent, code |

**Note**: App includes sample data generator - runs perfectly without CSV files!

---

## 🎯 Core Functionality

### Global Filter Architecture

**Sidebar Filters (Persistent Across Pages):**
```python
selected_countries = st.sidebar.multiselect("Select Countries", ...)
selected_sports = st.sidebar.multiselect("Select Sports", ...)
medal_types = st.sidebar.multiselect("Medal Types", ...)
selected_gender = st.sidebar.multiselect("Gender", ...)
```

All filters:
- ✅ Update charts in real-time
- ✅ Sync across all pages
- ✅ Persist using session state
- ✅ Have reasonable defaults

### Interactive Visualizations

- **Plotly Charts**: All charts are interactive (zoom, pan, hover)
- **Responsive Design**: Adapts to screen size using `use_container_width=True`
- **Color Schemes**: Professional, consistent color palettes

---

## 🔧 Customization Guide

### Add New Page

1. Create `pages/5_📱_New_Page.py`
2. Copy template from existing page:
   ```python
   import streamlit as st
   import pandas as pd
   import plotly.express as px
   
   st.set_page_config(page_title="New Page", page_icon="📱", layout="wide")
   
   # Load data
   # Get filters from session state
   # Create visualizations
   ```
3. Streamlit auto-loads from `pages/` folder

### Modify Colors

Edit design tokens in page files:
```python
color_discrete_map={
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
    'Bronze': '#CD7F32'
}
```

### Change Sample Data

Modify `load_data()` function in any page:
```python
@st.cache_data
def load_data():
    # Change this section
    countries = ['USA', 'China', 'France', ...]
    sports = ['Swimming', 'Track & Field', ...]
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution**: Use different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Charts not loading
**Solution**: Clear cache
```bash
streamlit run app.py --logger.level=debug
```

### Issue: Slow performance with large dataset
**Solution**: Add caching to data loading
```python
@st.cache_data
def load_data():
    # Data loads only once
```

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy with one click
4. Share URL with team

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 📈 Performance Tips

1. **Cache Data**:
   ```python
   @st.cache_data
   def load_data():
       return pd.read_csv('file.csv')
   ```

2. **Limit Chart Data**:
   ```python
   top_countries = medals['country'].value_counts().head(10)
   ```

3. **Use Session State**:
   ```python
   if 'data' not in st.session_state:
       st.session_state.data = load_data()
   ```

---

## 📝 Code Quality

- **Type Hints**: Clear function signatures
- **Docstrings**: Documented functions
- **Error Handling**: Try-except blocks for robustness
- **Comments**: Organized sections with headers

---

## 👥 Team Structure

**Recommended for 3-4 person team:**
- **Data Engineer**: Handles data loading and processing
- **Frontend Developer**: Manages page layouts and UI
- **Visualization Specialist**: Creates charts and reports
- **QA/DevOps**: Testing and deployment

---

## 📞 Support & Contributions

For issues or improvements:
1. Test thoroughly
2. Document changes
3. Submit pull request
4. Share feedback

---

## 📄 License

This project is provided as-is for the LA28 Olympic Games volunteer selection program.

---

## 🎓 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Guide**: https://plotly.com/python/
- **Pandas Tutorial**: https://pandas.pydata.org/docs/
- **Python Best Practices**: https://pep8.org/

---

## ✅ Checklist Before Submission

- [x] All 4 pages implemented
- [x] Global filters working
- [x] Charts responsive
- [x] Sample data generator included
- [x] Documentation complete
- [x] Code commented
- [x] No errors on startup
- [x] Performance optimized

---

## 📊 Sample Dashboard Statistics

**With Current Sample Data:**
- 👥 1,000+ Athletes
- 🌍 12 Countries
- 🏃 10 Sports
- 🥇 600+ Medals
- 🎯 500+ Events
- 🏟️ 15 Venues

---

---

🏅 **Good luck with LA28 volunteer selection! 🏅**
