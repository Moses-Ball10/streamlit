"""
1_🏠_Overview.py - The Command Center (MAIN ENTRY POINT)
Uses real Kaggle CSVs from ./data
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="🏠 Paris 2024 Olympics Dashboard",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
@st.cache_data
def load_data():
    """Load Paris 2024 Olympics dataset from ./data; fallback to sample."""
    try:
        athletes = pd.read_csv("data/athletes.csv")
        nocs = pd.read_csv("data/nocs.csv")  # code, country, ...
        events = pd.read_csv("data/events.csv")
        medals_total = pd.read_csv(
            "data/medals_total.csv"
        )  # country_code, country, Gold Medal, ...
        return athletes, nocs, events, medals_total
    except Exception:
        return generate_sample_data()


@st.cache_data
def generate_sample_data():
    """Sample data structurally similar to Kaggle dataset."""
    np.random.seed(42)

    codes = ["USA", "CHN", "FRA", "GBR", "JPN", "AUS", "GER", "ITA", "CAN", "NED"]
    country_names = [
        "United States",
        "China",
        "France",
        "Great Britain",
        "Japan",
        "Australia",
        "Germany",
        "Italy",
        "Canada",
        "Netherlands",
    ]

    n_athletes = 10000
    athletes = pd.DataFrame(
        {
            "athlete_id": range(1, n_athletes + 1),
            "name": [f"Athlete_{i}" for i in range(1, n_athletes + 1)],
            "country_code": np.random.choice(codes, n_athletes),
            "discipline": np.random.choice(
                ["Athletics", "Swimming", "Artistic Gymnastics", "Cycling Track"],
                n_athletes,
            ),
            "gender": np.random.choice(["M", "F"], n_athletes),
            "age": np.random.randint(16, 45, n_athletes),
            "height": np.random.randint(150, 210, n_athletes),
            "weight": np.random.randint(40, 120, n_athletes),
        }
    )

    nocs = pd.DataFrame(
        {
            "code": codes,
            "country": country_names,
            "country_long": country_names,
            "tag": [c.lower() for c in codes],
            "note": ["P"] * len(codes),
        }
    )

    sports = [
        "Athletics",
        "Swimming",
        "Artistic Gymnastics",
        "Cycling Track",
        "Basketball",
        "Football",
        "Tennis",
        "Rowing",
        "Sailing",
    ]
    n_events = 329
    events = pd.DataFrame(
        {
            "Discipline": np.random.choice(sports, n_events),
            "Event": [
                f"{sport} Event {i}"
                for i, sport in enumerate(np.random.choice(sports, n_events))
            ],
            "Event_gender": np.random.choice(["M", "F", "MIXED"], n_events),
            "venue_name": np.random.choice(
                ["Stade de France", "Aquatics Centre", "Velodrome"], n_events
            ),
            "slug": [f"event-{i}" for i in range(n_events)],
        }
    )

    medals_total = pd.DataFrame(
        {
            "country_code": codes,
            "country": country_names,
            "country_long": country_names,
            "Gold Medal": np.random.randint(0, 50, len(codes)),
            "Silver Medal": np.random.randint(0, 40, len(codes)),
            "Bronze Medal": np.random.randint(0, 35, len(codes)),
            "Total": np.random.randint(10, 120, len(codes)),
        }
    )

    return athletes, nocs, events, medals_total


# Load data
athletes, nocs, events, medals_total = load_data()

# --------------------------------------------------
# COLUMN HARMONISATION
# --------------------------------------------------
# common NOC code column
nocs["noc_code"] = nocs["code"]
medals_total["noc_code"] = medals_total["country_code"]

# NOC column in athletes.csv
ath_noc_col = "country_code"  # from your dataset

# discipline / sport column in events
if "Discipline" in events.columns:
    sport_col = "Discipline"
elif "discipline" in events.columns:
    sport_col = "discipline"
else:
    sport_col = "sport"  # fallback

# --------------------------------------------------
# GLOBAL FILTERS
# --------------------------------------------------
st.sidebar.title("🌍 Global Filters")
st.sidebar.markdown("---")

all_nocs = sorted(nocs["noc_code"].unique())
all_sports = sorted(events[sport_col].unique())

if "filters_initialized" not in st.session_state:
    st.session_state.selected_nocs = all_nocs  # start with ALL codes
    st.session_state.selected_sports = all_sports  # start with ALL sports
    st.session_state.filters_initialized = True

selected_nocs = st.sidebar.multiselect(
    "🏆 Country (NOC code)",
    options=all_nocs,
    default=st.session_state.selected_nocs,
    key="noc_filter",
)

selected_sports = st.sidebar.multiselect(
    "⚽ Sport / Discipline",
    options=all_sports,
    default=st.session_state.selected_sports,
    key="sport_filter",
)

st.session_state.selected_nocs = selected_nocs
st.session_state.selected_sports = selected_sports

st.sidebar.markdown("---")


# --------------------------------------------------
# FILTERING LOGIC
# --------------------------------------------------
def apply_filters():
    final_nocs = selected_nocs if selected_nocs else all_nocs

    fa = athletes[athletes[ath_noc_col].isin(final_nocs)].copy()
    if sport_col in fa.columns:
        fa = fa[fa[sport_col].isin(selected_sports)]

    fe = events[events[sport_col].isin(selected_sports)].copy()

    fm = medals_total[medals_total["noc_code"].isin(final_nocs)].copy()

    return fa, fe, fm


filtered_athletes, filtered_events, filtered_medals = apply_filters()

# share for other pages
st.session_state.filtered_athletes = filtered_athletes
st.session_state.filtered_events = filtered_events
st.session_state.filtered_medals = filtered_medals
st.session_state.raw_data = {
    "athletes": athletes,
    "nocs": nocs,
    "events": events,
    "medals_total": medals_total,
}

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
<div style='text-align: center; padding: 3rem 0 2rem 0; background: linear-gradient(135deg, #1f77b4 0%, #4a90e2 100%); 
            border-radius: 20px; margin-bottom: 2rem; color: white;'>
    <h1 style='font-size: 4rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🥇 Paris 2024 Olympics Dashboard</h1>
    <p style='font-size: 1.5rem; margin: 1rem 0 0 0; opacity: 0.95;'>
        <strong>Comprehensive analysis</strong> of athlete performance, global rankings, and event insights
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
st.markdown("## 📊 Key Performance Indicators")

kpi_cols = st.columns(5)
with kpi_cols[0]:
    total_athletes = len(filtered_athletes)
    st.metric("👥 Total Athletes", f"{total_athletes:,}", delta=f"of {len(athletes):,}")

with kpi_cols[1]:
    total_countries = filtered_medals["country"].nunique()
    st.metric("🌍 Total Countries", f"{total_countries:,}", delta=f"of {len(nocs):,}")

with kpi_cols[2]:
    total_sports = filtered_events[sport_col].nunique()
    st.metric(
        "⚽ Total Sports",
        total_sports,
        delta=f"of {events[sport_col].nunique()}",
    )

with kpi_cols[3]:
    total_medals_awarded = filtered_medals["Total"].sum()
    st.metric("🏅 Total Medals", f"{int(total_medals_awarded):,}", delta="awarded")

with kpi_cols[4]:
    num_events = len(filtered_events)
    st.metric("🎯 Number of Events", f"{num_events:,}", delta="total competitions")

st.markdown("---")

# --------------------------------------------------
# VISUALISATIONS
# --------------------------------------------------
viz_cols = st.columns([2, 1.2])

with viz_cols[0]:
    st.markdown("### 🏅 Global Medal Distribution")
    medal_totals = filtered_medals[["Gold Medal", "Silver Medal", "Bronze Medal"]].sum()

    fig_pie = px.pie(
        values=[
            medal_totals.get("Gold Medal", 0),
            medal_totals.get("Silver Medal", 0),
            medal_totals.get("Bronze Medal", 0),
        ],
        names=["Gold", "Silver", "Bronze"],
        hole=0.45,
        color_discrete_map={
            "Gold": "#FFD700",
            "Silver": "#C0C0C0",
            "Bronze": "#CD7F32",
        },
        title="Gold : Silver : Bronze Distribution",
    )
    fig_pie.update_layout(height=450, showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

with viz_cols[1]:
    st.markdown("### 🥇 Top 10 Medal Standings")
    tmp = filtered_medals.sort_values("Total", ascending=False).head(10)
    top_10 = tmp[["country", "Total"]].copy()
    top_10.columns = ["Country", "Total"]

    fig_bar = px.bar(
        top_10,
        x="Total",
        y="Country",
        orientation="h",
        color="Total",
        color_continuous_scale="Viridis_r",
        title="Top 10 Countries",
    )
    fig_bar.update_layout(height=450, showlegend=False, xaxis_title="Total Medals")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
