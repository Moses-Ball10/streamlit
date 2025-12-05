import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

# ===============================
# Data loading
# ===============================


@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"

    athletes = pd.read_csv(data_dir / "athletes.csv")
    coaches = pd.read_csv(data_dir / "coaches.csv")
    teams = pd.read_csv(data_dir / "teams.csv")
    medals = pd.read_csv(data_dir / "medals.csv")
    medallists = pd.read_csv(data_dir / "medallists.csv")
    nocs = pd.read_csv(data_dir / "nocs.csv")  # code,country,country_long,tag,note
    return athletes, coaches, teams, medals, medallists, nocs


athletes, coaches, teams, medals, medallists, nocs = load_data()

# ===============================
# Derived fields
# ===============================

# Age from birth_date
if "birth_date" in athletes.columns:
    reference_date = pd.Timestamp("2024-07-26")  # Paris 2024 opening day [web:1]
    athletes["birth_date"] = pd.to_datetime(
        athletes["birth_date"], format="%Y-%m-%d", errors="coerce"
    )
    athletes["age"] = (reference_date - athletes["birth_date"]).dt.days // 365
else:
    athletes["age"] = pd.NA

# Build athletes_geo with country + continent using NOCs
athletes_geo = athletes.copy()
if not nocs.empty and "country_code" in athletes_geo.columns and "code" in nocs.columns:
    nocs_tmp = nocs.rename(columns={"code": "country_code"})
    if "country_long" in nocs_tmp.columns:
        nocs_tmp = nocs_tmp.rename(columns={"country_long": "country"})
    else:
        nocs_tmp = nocs_tmp.rename(columns={"country": "country"})

    # simple continent mapping (extend later if you like)
    noc_to_continent = {
        "ALG": "Africa",
        "EGY": "Africa",
        "KEN": "Africa",
        "RSA": "Africa",
        "NGR": "Africa",
        "NIG": "Africa",
        "USA": "Americas",
        "CAN": "Americas",
        "MEX": "Americas",
        "BRA": "Americas",
        "ARG": "Americas",
        "CHI": "Americas",
        "COL": "Americas",
        "CHN": "Asia",
        "JPN": "Asia",
        "KOR": "Asia",
        "IND": "Asia",
        "INA": "Asia",
        "AUS": "Oceania",
        "NZL": "Oceania",
        "FRA": "Europe",
        "GER": "Europe",
        "GBR": "Europe",
        "ESP": "Europe",
        "ITA": "Europe",
        "NED": "Europe",
        "SWE": "Europe",
        "DEN": "Europe",
        "NOR": "Europe",
        "SUI": "Europe",
    }
    nocs_tmp["continent"] = (
        nocs_tmp["country_code"].map(noc_to_continent).fillna("Other")
    )

    athletes_geo = athletes_geo.merge(
        nocs_tmp[["country_code", "country", "continent"]],
        on="country_code",
        how="left",
    )

if "country" not in athletes_geo.columns:
    if "country" in athletes.columns:
        athletes_geo["country"] = athletes["country"]
    else:
        athletes_geo["country"] = athletes_geo.get("country_code", "Unknown")

if "continent" not in athletes_geo.columns:
    athletes_geo["continent"] = "Other"
# ensure unique column names on athletes_geo
athletes_geo = athletes_geo.loc[:, ~athletes_geo.columns.duplicated()]

# ===============================
# 🌍 Global Filters (sidebar)
# ===============================

with st.sidebar:
    st.markdown("## 🌍 Global Filters")

    # Continent
    cont_options = sorted(athletes_geo["continent"].dropna().unique())
    selected_continents = st.multiselect(
        "🌐 Continent",
        options=cont_options,
        default=cont_options,
    )

    # Country
    country_options = sorted(athletes_geo["country"].dropna().unique())
    selected_countries = st.multiselect(
        "🏳️ Country",
        options=country_options,
        default=country_options,
    )

    # Sport
    sport_options = (
        sorted(athletes["sport"].dropna().unique())
        if "sport" in athletes.columns
        else []
    )
    selected_sports = st.multiselect(
        "🏅 Sport",
        options=sport_options,
        default=sport_options,
    )

    # Medal types (from medallists)
    medal_type_options = (
        sorted(medallists["medal_type"].dropna().unique())
        if "medal_type" in medallists.columns
        else []
    )
    selected_medal_types = st.multiselect(
        "🥇 Medal Types",
        options=medal_type_options,
        default=medal_type_options,
    )

# Apply filters to athletes / medallists
filtered_athletes = athletes_geo.copy()


if selected_continents:
    filtered_athletes = filtered_athletes[
        filtered_athletes["continent"].isin(selected_continents)
    ]
if selected_countries:
    filtered_athletes = filtered_athletes[
        filtered_athletes["country"].isin(selected_countries)
    ]
if selected_sports and "sport" in filtered_athletes.columns:
    filtered_athletes = filtered_athletes[
        filtered_athletes["sport"].isin(selected_sports)
    ]

filtered_medals = medallists.copy()
if "is_medallist" in filtered_medals.columns:
    filtered_medals = filtered_medals[filtered_medals["is_medallist"] == 1]
if selected_countries and "country" in filtered_medals.columns:
    filtered_medals = filtered_medals[
        filtered_medals["country"].isin(selected_countries)
    ]
if selected_sports and "discipline" in filtered_medals.columns:
    filtered_medals = filtered_medals[
        filtered_medals["discipline"].isin(selected_sports)
    ]
if selected_medal_types:
    filtered_medals = filtered_medals[
        filtered_medals["medal_type"].isin(selected_medal_types)
    ]
filtered_athletes = filtered_athletes.loc[:, ~filtered_athletes.columns.duplicated()]

# ===============================
# Page title
# ===============================


st.markdown(
    """
<div style="text-align:center; padding: 1.5rem 0;">
  <h1 style="color:#2e86ab;">👤 Athlete Performance – The Human Story</h1>
  <p style="color:#555; font-size:1.1rem;">
    Interactive exploration of individual athletes’ stories, combining profiles, demographics, and medal achievements to highlight human performance at Paris 2024.
  </p>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("---")

# ===============================
# Athlete Detailed Profile Card
# ===============================

st.subheader("Athlete Detailed Profile")

athlete_name = st.selectbox(
    "Select an athlete",
    options=sorted(filtered_athletes["name"].dropna().unique()),
    index=None,
    placeholder="Start typing a name…",
)

if athlete_name:
    a = filtered_athletes[filtered_athletes["name"] == athlete_name].iloc[0]

    # Coaches from athletes.coach
    coach_names = None
    if (
        "coach" in filtered_athletes.columns
        and pd.notna(a.get("coach", None))
        and str(a["coach"]).strip()
    ):
        coach_names = str(a["coach"]).strip()
    if not coach_names:
        coach_names = "N/A"

    # Sports & disciplines
    sports = (
        ", ".join(sorted({str(a["sport"])}))
        if "sport" in filtered_athletes.columns
        else "N/A"
    )
    if "disciplines" in filtered_athletes.columns and pd.notna(a["disciplines"]):
        disciplines = ", ".join(str(a["disciplines"]).split(";"))
    else:
        disciplines = "N/A"

    # Country / NOC via nocs
    noc = a.get("country_code", None)
    country_display = a.get("country", None)
    if noc and "code" in nocs.columns:
        match = nocs[nocs["code"] == noc]
        if not match.empty:
            country_display = match["country_long"].iloc[0]
    country_display = country_display or noc or "N/A"
    flag = ""

    col_img, col_main = st.columns([1, 2])

    with col_img:
        img_col = None
        for c in ["image_url", "photo", "profile_image"]:
            if c in filtered_athletes.columns:
                img_col = c
                break

        if img_col and pd.notna(a[img_col]):
            st.image(a[img_col], use_column_width=True)
        else:
            st.markdown(
                """
                <div style="
                    width:100%;
                    aspect-ratio:3/4;
                    border-radius:12px;
                    background:linear-gradient(135deg,#1f77b4,#ff7f0e);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:32px;
                    font-weight:700;
                ">
                    ATH
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_main:
        st.markdown(f"### {a['name']}")
        st.markdown(f"**Country / NOC:** {country_display} {flag}  (`{noc}`)")
        if "gender" in a:
            st.markdown(f"**Gender:** {a['gender']}")
        height_val = a.get("height", "N/A")
        weight_val = a.get("weight", "N/A")
        st.markdown(
            f"**Height:** {height_val} cm &nbsp;&nbsp; **Weight:** {weight_val} kg"
        )
        if "age" in a and pd.notna(a["age"]):
            st.markdown(f"**Age (at Paris 2024):** {int(a['age'])} years")
        st.markdown(f"**Coach(s):** {coach_names}")
        st.markdown(f"**Sport(s):** {sports}")
        st.markdown(f"**Discipline(s):** {disciplines}")

# ===============================
# Athlete Age Distribution
# ===============================

st.subheader("Athlete Age Distribution")

df_age = filtered_athletes.dropna(subset=["age"]).copy()

plot_type = st.radio("Plot type", ["Violin", "Box"], horizontal=True)
group_by = st.selectbox("Group age by", ["Sport", "Gender", "All athletes"])

if df_age.empty:
    st.info("No valid age information available to plot age distribution.")
else:
    if group_by == "Sport" and "sport" in df_age.columns:
        x_col = "sport"
    elif group_by == "Gender" and "gender" in df_age.columns:
        x_col = "gender"
    else:
        x_col = None

    if plot_type == "Violin":
        if x_col:
            fig_age = px.violin(
                df_age,
                x=x_col,
                y="age",
                color=x_col,
                box=True,
                points="all",
                height=500,
            )
        else:
            fig_age = px.violin(df_age, y="age", box=True, points="all", height=400)
    else:
        if x_col:
            fig_age = px.box(
                df_age, x=x_col, y="age", color=x_col, points="all", height=500
            )
        else:
            fig_age = px.box(df_age, y="age", points="all", height=400)

    fig_age.update_layout(xaxis_title="", yaxis_title="Age (years)")
    st.plotly_chart(fig_age, use_container_width=True)

# ===============================
# Gender Distribution by Region
# ===============================

st.subheader("Gender Distribution by Region")

scope = st.radio("Scope", ["Continent", "Country"], horizontal=True)

if scope == "Continent":
    cont_options = sorted(filtered_athletes["continent"].dropna().unique())
    selected_cont = (
        st.selectbox("Select continent", cont_options) if cont_options else None
    )
    df_g = (
        filtered_athletes[filtered_athletes["continent"] == selected_cont]
        if selected_cont
        else filtered_athletes
    )
else:
    country_options = sorted(filtered_athletes["country"].dropna().unique())
    ctry = st.selectbox("Select country", country_options) if country_options else None
    df_g = (
        filtered_athletes[filtered_athletes["country"] == ctry]
        if ctry
        else filtered_athletes
    )

if not df_g.empty and "gender" in df_g.columns:
    gender_counts = df_g["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]

    chart_type = st.radio("Chart type", ["Pie", "Bar"], horizontal=True)

    if chart_type == "Pie":
        fig_gender = px.pie(
            gender_counts,
            names="gender",
            values="count",
            hole=0.3,
        )
    else:
        fig_gender = px.bar(
            gender_counts,
            x="gender",
            y="count",
            text="count",
        )
        fig_gender.update_layout(yaxis_title="Number of athletes")

    st.plotly_chart(fig_gender, use_container_width=True)
else:
    st.info("No gender data available for the selected filter.")

# ===============================
# Top Athletes by Total Medals
# ===============================

st.subheader("Top Athletes by Total Medals")

df_medals = filtered_medals.copy()

if not df_medals.empty:
    medals_per_athlete = (
        df_medals.groupby("name")["medal_type"]
        .count()
        .reset_index()
        .rename(columns={"medal_type": "total_medals"})
    )

    top_medals = medals_per_athlete.sort_values("total_medals", ascending=False).head(
        10
    )

    fig_top = px.bar(
        top_medals,
        x="name",
        y="total_medals",
        text="total_medals",
    )
    fig_top.update_traces(textposition="outside")
    fig_top.update_layout(
        xaxis_title="Athlete",
        yaxis_title="Total medals",
        xaxis_tickangle=-40,
        showlegend=False,
    )

    st.plotly_chart(fig_top, use_container_width=True)
else:
    st.info("No medalist records available to plot top athletes.")
