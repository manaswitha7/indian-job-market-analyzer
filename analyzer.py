import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Indian Job Market Intelligence Platform",
    layout="wide"
)

# Load Data


@st.cache_data
def load_data():
    return pd.read_csv("data/jobs.csv")


df = load_data()

st.title("🇮🇳 Indian Job Market Intelligence Platform")

# Sidebar Filters
st.sidebar.header("Filters")

cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["location"].dropna().unique())
)

roles = st.sidebar.multiselect(
    "Select Job Role",
    options=sorted(df["title"].dropna().unique())
)

filtered_df = df.copy()

if cities:
    filtered_df = filtered_df[
        filtered_df["location"].isin(cities)
    ]

if roles:
    filtered_df = filtered_df[
        filtered_df["title"].isin(roles)
    ]

# KPIs
st.subheader("Market Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Jobs",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Companies",
        filtered_df["companyName"].nunique()
    )

with col3:
    st.metric(
        "Cities",
        filtered_df["location"].nunique()
    )

# Top Cities
st.subheader("Top Hiring Cities")

top_cities = (
    filtered_df["location"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=top_cities.index,
    y=top_cities.values,
    labels={
        "x": "City",
        "y": "Jobs"
    }
)

st.plotly_chart(fig, use_container_width=True)

# Top Companies
st.subheader("Top Hiring Companies")

top_companies = (
    filtered_df["companyName"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=top_companies.index,
    y=top_companies.values
)

st.plotly_chart(fig, use_container_width=True)

# Skills Analysis
st.subheader("Most Demanded Skills")

skills = []

for row in filtered_df["tagsAndSkills"].dropna():
    skills.extend(
        [s.strip() for s in str(row).split(",")]
    )

skill_counts = (
    pd.Series(skills)
    .value_counts()
    .head(20)
)

fig = px.bar(
    x=skill_counts.index,
    y=skill_counts.values
)

st.plotly_chart(fig, use_container_width=True)

# Salary Analysis
st.subheader("Salary Distribution")

filtered_df["averageSalary"] = (
    pd.to_numeric(
        filtered_df["minimumSalary"],
        errors="coerce"
    )
    +
    pd.to_numeric(
        filtered_df["maximumSalary"],
        errors="coerce"
    )
) / 2

fig = px.histogram(
    filtered_df,
    x="averageSalary",
    nbins=30
)

st.plotly_chart(fig, use_container_width=True)

# Career Recommendation
st.subheader("Career Skill Recommender")

career = st.text_input(
    "Enter a Role",
    "Data Analyst"
)

if st.button("Recommend Skills"):

    role_df = filtered_df[
        filtered_df["title"]
        .str.contains(
            career,
            case=False,
            na=False
        )
    ]

    role_skills = []

    for row in role_df["tagsAndSkills"].dropna():
        role_skills.extend(
            [s.strip()
             for s in str(row).split(",")]
        )

    recommendations = (
        pd.Series(role_skills)
        .value_counts()
        .head(10)
    )

    st.write(
        f"Top Skills for {career}"
    )

    st.dataframe(
        recommendations.reset_index()
    )
