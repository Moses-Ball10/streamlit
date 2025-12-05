# pages/2_🗺️_Global_Analysis.py  (replace the whole file with this)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Global Analysis", page_icon="🗺️", layout="wide")


@st.cache_data
@st.cache_data
def load_data():
    """Load medals + nocs, fallback to sample if files missing."""
    try:
        medals = pd.read_csv("../data/medals.csv")
        nocs = pd.read_csv("../data/nocs.csv")  # uses the true continent from Kaggle
    except Exception:
        np.random.seed(42)
        countries = [
            "USA",
            "China",
            "France",
            "GB",
            "Japan",
            "Australia",
            "Germany",
            "Italy",
            "Spain",
            "Canada",
            "Korea",
            "Netherlands",
        ]
        sports = [
            "Swimming",
            "Track",
            "Gymnastics",
            "Basketball",
            "Tennis",
            "Volleyball",
            "Cycling",
            "Rowing",
            "Archery",
            "Badminton",
        ]
        medals = pd.DataFrame(
            {
                "medal_id": range(1, 601),
                "country": np.random.choice(countries, 600),
                "sport": np.random.choice(sports, 600),
                "medal_type": np.random.choice(
                    ["Gold", "Silver", "Bronze"], 600, p=[0.3, 0.35, 0.35]
                ),
            }
        )
        # deterministic, correct continent mapping for the sample
        nocs = pd.DataFrame(
            {
                "country": countries,
                "continent": [
                    "Americas",  # USA
                    "Asia",  # China
                    "Europe",  # France
                    "Europe",  # GB
                    "Asia",  # Japan
                    "Oceania",  # Australia
                    "Europe",  # Germany
                    "Europe",  # Italy
                    "Europe",  # Spain
                    "Americas",  # Canada
                    "Asia",  # Korea
                    "Europe",  # Netherlands
                ],
            }
        )
    return medals, nocs


medals, nocs = (
    load_data()
)  # medals: country, sport, medal_type; nocs: country, continent

# -------------------------------------------------------------------
# GLOBAL FILTERS (use same names as app.py sidebar state)
# -------------------------------------------------------------------
st.sidebar.title("🌍 Global Filters")
st.sidebar.markdown("---")

all_countries = sorted(medals["country"].unique())
all_sports = sorted(medals["sport"].unique())
all_continents = sorted(nocs["continent"].unique())

# Read defaults from session_state if present, else use full lists
default_countries = st.session_state.get("countries", all_countries)
default_sports = st.session_state.get("sports", all_sports)
default_medals = st.session_state.get("medals", ["Gold", "Silver", "Bronze"])

# Continent filter
selected_continents = st.sidebar.multiselect(
    "🌎 Continent",
    options=all_continents,
    default=all_continents,
    key="continent_global",
)

# Restrict countries by selected continents
if selected_continents:
    allowed_countries = nocs[nocs["continent"].isin(selected_continents)][
        "country"
    ].unique()
    allowed_countries = sorted(list(allowed_countries))
else:
    allowed_countries = all_countries

selected_countries = st.sidebar.multiselect(
    "🏳️ Country",
    options=allowed_countries,
    default=[c for c in default_countries if c in allowed_countries]
    or allowed_countries,
    key="countries_global",
)

selected_sports = st.sidebar.multiselect(
    "🏅 Sport",
    options=all_sports,
    default=default_sports,
    key="sports_global",
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎖 Medal Types")
selected_medal_types = st.sidebar.multiselect(
    "Select medal types",
    options=["Gold", "Silver", "Bronze"],
    default=default_medals,
    key="medaltypes_global",
)

st.sidebar.markdown("---")
st.sidebar.info("Filters update all visualizations on this page.")

# -------------------------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------------------------
filtered_medals = medals[
    medals["country"].isin(selected_countries)
    & medals["sport"].isin(selected_sports)
    & medals["medal_type"].isin(selected_medal_types)
].copy()

# Attach continent ONCE here – guarantees column exists
filtered_medals = filtered_medals.merge(nocs, on="country", how="left")

# -------------------------------------------------------------------
# PAGE TITLE
# -------------------------------------------------------------------
st.markdown(
    """
<div style="text-align:center; padding: 1.5rem 0;">
  <h1 style="color:#2e86ab;">🗺️ Global Analysis - The World View</h1>
  <p style="color:#555; font-size:1.1rem;">
    Geographical and hierarchical view of Olympic medal performance by continent and country.
  </p>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("---")

if filtered_medals.empty:
    st.warning("No data for the current filter selection.")
    st.stop()

# -------------------------------------------------------------------
# 1. WORLD MEDAL MAP (Choropleth)
# -------------------------------------------------------------------
st.subheader("🌍 World Medal Map")

country_totals = (
    filtered_medals.groupby("country")["medal_type"]
    .count()
    .reset_index(name="total_medals")
)

# Simple mapping for demo; adjust to your NOC/ISO mapping if needed
name_to_iso = {
    "USA": "USA",
    "United States": "USA",
    "China": "CHN",
    "France": "FRA",
    "GB": "GBR",
    "Great Britain": "GBR",
    "Japan": "JPN",
    "Australia": "AUS",
    "Germany": "DEU",
    "Italy": "ITA",
    "Spain": "ESP",
    "Canada": "CAN",
    "Korea": "KOR",
    "Netherlands": "NLD",
}
country_totals["iso_alpha"] = country_totals["country"].map(name_to_iso)

fig_world = px.choropleth(
    country_totals,
    locations="iso_alpha",
    color="total_medals",
    hover_name="country",
    color_continuous_scale="Viridis",
    title="Total Medals by Country",
)
fig_world.update_layout(height=500, margin=dict(l=0, r=0, t=60, b=0))
st.plotly_chart(fig_world, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# 2. MEDAL HIERARCHY BY CONTINENT (Sunburst + Treemap)
#    Continent -> Country -> Sport -> Medal Count
# -------------------------------------------------------------------
st.subheader("📊 Medal Hierarchy by Continent")

# Aggregate counts for hierarchy
hierarchy_df = (
    filtered_medals.groupby(["continent", "country", "sport", "medal_type"])
    .size()
    .reset_index(name="count")
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ☀️ Sunburst")
    fig_sunburst = px.sunburst(
        hierarchy_df,
        path=["continent", "country", "sport", "medal_type"],
        values="count",
        color="count",
        color_continuous_scale="RdYlGn",
    )
    fig_sunburst.update_layout(height=450)
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    st.markdown("#### 🧩 Treemap")
    fig_treemap = px.treemap(
        hierarchy_df,
        path=["continent", "country", "sport", "medal_type"],
        values="count",
        color="count",
        color_continuous_scale="RdYlGn",
    )
    fig_treemap.update_layout(height=450)
    st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# 3. CONTINENT VS MEDALS (Grouped Bar)
# -------------------------------------------------------------------
st.subheader("🌎 Continent vs. Medals")

continent_medals = filtered_medals.pivot_table(
    index="continent",
    columns="medal_type",
    values="medal_id" if "medal_id" in filtered_medals.columns else "country",
    aggfunc="count",
    fill_value=0,
).reset_index()

# Ensure all medal columns exist
for m in ["Gold", "Silver", "Bronze"]:
    if m not in continent_medals.columns:
        continent_medals[m] = 0

fig_continent = px.bar(
    continent_medals,
    x="continent",
    y=["Gold", "Silver", "Bronze"],
    barmode="group",
    color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"},
    title="Gold, Silver, Bronze Medals by Continent",
)
fig_continent.update_layout(
    height=450, xaxis_title="Continent", yaxis_title="Medal Count"
)
st.plotly_chart(fig_continent, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# 4. COUNTRY VS MEDALS (Top 20, Grouped Bar)
# -------------------------------------------------------------------
selected_countries = st.session_state.get("countries", list(medals["country"].unique()))
selected_sports = st.session_state.get("sports", list(medals["sport"].unique()))
medal_types = st.session_state.get("medals", ["Gold", "Silver", "Bronze"])

filtered_medals = medals[
    (medals["country"].isin(selected_countries))
    & (medals["sport"].isin(selected_sports))
    & (medals["medal_type"].isin(medal_types))
]
filtered_medals = filtered_medals.merge(nocs, on="country", how="left")


if len(filtered_medals) > 0:
    st.subheader("📊 Medals by Country")
    medal_by_country = filtered_medals["country"].value_counts().head(20)
    fig = px.bar(
        x=medal_by_country.index,
        y=medal_by_country.values,
        color=medal_by_country.values,
        labels={"x": "Country", "y": "Number of Medals"},
        title="Top 20 Countries by Medals",
    )
    st.plotly_chart(fig, use_container_width=True)
