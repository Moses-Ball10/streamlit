import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ===============================
# Data loading
# ===============================


@st.cache_data
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"

    events = pd.read_csv(data_dir / "events.csv")
    medallists = pd.read_csv(data_dir / "medallists.csv")
    venues = pd.read_csv(data_dir / "venues.csv")

    # Try to load coordinates; if missing, just continue without them
    # Hard-coded coordinates for main Paris 2024 venues
    venue_coords = {
        "Aquatics Centre": (48.9235, 2.3560),
        "Bercy Arena": (48.8386, 2.3781),
        "Bordeaux Stadium": (44.8973, -0.5619),
        "Champ de Mars Arena": (48.8558, 2.2983),
        "Château de Versailles": (48.8059, 2.1204),
        "Chateauroux Shooting Centre": (46.8151, 1.7566),
        "Eiffel Tower Stadium": (48.8570, 2.2980),
        "Elancourt Hill": (48.7883, 1.9677),
        "Geoffroy-Guichard Stadium": (45.4605, 4.3892),
        "Grand Palais": (48.8660, 2.3117),
        "Hôtel de Ville": (48.8566, 2.3522),
        "Invalides": (48.8565, 2.3124),
        "La Beaujoire Stadium": (47.2560, -1.5250),
        "La Concorde": (48.8656, 2.3211),
        "Le Bourget Sport Climbing Venue": (48.9373, 2.4200),
        "Golf National": (48.7546, 2.0760),
        "Lyon Stadium": (45.7653, 4.9818),
        "Marseille Marina": (43.2951, 5.3643),
        "Marseille Stadium": (43.2699, 5.3958),
        "Nice Stadium": (43.7052, 7.1926),
        "North Paris Arena": (48.9466, 2.4194),
        "Parc des Princes": (48.8414, 2.2528),
        "Paris La Defense Arena": (48.8947, 2.2296),
        "Pierre Mauroy Stadium": (50.6118, 3.1300),
        "Pont Alexandre III": (48.8650, 2.3130),
        "Porte de La Chapelle Arena": (48.8994, 2.3597),
        "Stade Roland-Garros": (48.8459, 2.2537),
        "Saint-Quentin-en-Yvelines BMX Stadium": (48.7883, 2.0400),
        "Saint-Quentin-en-Yvelines Velodrome": (48.7880, 2.0345),
        "South Paris Arena": (48.8301, 2.2903),  # Porte de Versailles area
        "Stade de France": (48.9245, 2.3597),
        "Teahupo'o, Tahiti": (-17.8095, -149.3034),
        "Trocadéro": (48.8616, 2.2890),
        "Vaires-sur-Marne Nautical Stadium": (48.8604, 2.6373),
        "Yves-du-Manoir Stadium": (48.9293, 2.2476),
    }

    coord_df = (
        pd.DataFrame.from_dict(
            venue_coords, orient="index", columns=["latitude", "longitude"]
        )
        .reset_index()
        .rename(columns={"index": "venue"})
    )

    # merge into venues
    venues = venues.merge(coord_df, on="venue", how="left")

    return events, medallists, venues


events, medallists, venues = load_data()

# Parse venue date ranges
venues["date_start"] = pd.to_datetime(venues["date_start"], errors="coerce")
venues["date_end"] = pd.to_datetime(venues["date_end"], errors="coerce")

# ===============================
# Sidebar – Global Filters
# ===============================

with st.sidebar:
    st.markdown("## 🌍 Global Filters")

    # Sport options from events
    sport_options = sorted(events["sport"].dropna().unique())
    selected_sports = st.multiselect(
        "🏅 Sport",
        options=sport_options,
        default=sport_options,
    )

    # Medal type options from medallists
    medal_type_options = sorted(medallists["medal_type"].dropna().unique())
    selected_medal_types = st.multiselect(
        "🥇 Medal type",
        options=medal_type_options,
        default=medal_type_options,
    )

# Filter events by sport
filtered_events = events.copy()
if selected_sports:
    filtered_events = filtered_events[filtered_events["sport"].isin(selected_sports)]

# Filter medals by sport (discipline) and medal type
filtered_medals = medallists.copy()
if "is_medallist" in filtered_medals.columns:
    filtered_medals = filtered_medals[filtered_medals["is_medallist"] == True]

if selected_sports:
    filtered_medals = filtered_medals[
        filtered_medals["discipline"].isin(selected_sports)
    ]

if selected_medal_types:
    filtered_medals = filtered_medals[
        filtered_medals["medal_type"].isin(selected_medal_types)
    ]

# Filter venues by sport list string
filtered_venues = venues.copy()
if selected_sports:
    pattern = "|".join(selected_sports)
    filtered_venues = filtered_venues[
        filtered_venues["sports"].str.contains(pattern, regex=True)
    ]

# ===============================
# Page title
# ===============================

st.markdown(
    """
<div style="text-align:center; padding: 1.5rem 0;">
  <h1 style="color:#2e86ab;">🏟️ Sports & Events – The Competition Arena</h1>
  <p style="color:#555; font-size:1.1rem;">
Interactive exploration of Olympic sports, event schedules, medal outcomes, and venues across Paris.  </p>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("---")

# ===============================
# Event Schedule (Gantt via venues)
# ===============================

st.subheader("Event Schedule by Venue")

if filtered_venues.empty:
    st.info("No venues match the current filters.")
else:
    df_sched = filtered_venues.copy()

    # Color by main sport (first element in sports list)
    df_sched["main_sport"] = (
        df_sched["sports"].str.strip("[]").str.split(",").str[0].str.strip(" '\"")
    )

    fig_sched = px.timeline(
        df_sched,
        x_start="date_start",
        x_end="date_end",
        y="venue",
        color="main_sport",
        hover_data=["sports"],
    )
    fig_sched.update_yaxes(autorange="reversed")
    fig_sched.update_layout(
        xaxis_title="Date",
        yaxis_title="Venue",
        height=500,
    )
    st.plotly_chart(fig_sched, use_container_width=True)

# ===============================
# Medal Count by Sport (Treemap)
# ===============================

st.subheader("Medal Count by Sport")

if filtered_medals.empty:
    st.info("No medal data available for the current filters.")
else:
    medals_by_sport = (
        filtered_medals.groupby("discipline")["medal_type"]
        .count()
        .reset_index()
        .rename(columns={"discipline": "sport", "medal_type": "total_medals"})
    )

    fig_treemap = px.treemap(
        medals_by_sport,
        path=["sport"],
        values="total_medals",
        color="total_medals",
        color_continuous_scale="Blues",
    )
    fig_treemap.update_layout(margin=dict(t=40, l=10, r=10, b=10))
    st.plotly_chart(fig_treemap, use_container_width=True)

# ===============================
# Venue Map (Scatter Mapbox)
# ===============================

st.subheader("Venue Map")

coord_ok = {"latitude", "longitude"}.issubset(venues.columns)
filtered_venues_map = (
    filtered_venues.dropna(subset=["latitude", "longitude"])
    if coord_ok
    else pd.DataFrame()
)

if not coord_ok or filtered_venues_map.empty:
    st.info(
        "No venue coordinates available. Make sure venue_coords.csv "
        "has latitude/longitude for each venue and the names match venues.csv."
    )
else:
    fig_map = px.scatter_mapbox(
        filtered_venues_map,
        lat="latitude",
        lon="longitude",
        hover_name="venue",
        hover_data=["sports"],
        zoom=4,
        height=600,
    )
    fig_map.update_layout(
        mapbox_style="carto-positron",
        margin=dict(t=20, l=0, r=0, b=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)
