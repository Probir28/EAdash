import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filter Data")
departments = st.sidebar.multiselect("Select Department(s):", options=df["Department"].unique(), default=df["Department"].unique())
genders = st.sidebar.multiselect("Select Gender:", options=df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("Select Age Range:", int(df["Age"].min()), int(df["Age"].max()), (25, 50))

filtered_df = df[
    (df["Department"].isin(departments)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# Main header
st.title("📊 HR Attrition Insight Dashboard")
st.markdown("An interactive dashboard to help HR stakeholders analyze employee attrition trends, drivers, and workforce insights.")

st.markdown("---")

# Tab Layout
tabs = st.tabs([
    "📌 Overview", "📉 Attrition Trends", "🏢 Departmental Insights", "🧠 Satisfaction & Performance",
    "📅 Experience & Tenure", "📦 Compensation Analysis", "📍 Custom Plots"
])

# 1. Overview
with tabs[0]:
    st.subheader("Attrition Distribution")
    st.markdown("This pie chart shows the overall attrition status.")
    pie_chart = px.pie(filtered_df, names="Attrition", title="Overall Attrition Distribution")
    st.plotly_chart(pie_chart, use_container_width=True)

    st.markdown("Bar chart of gender vs attrition")
    fig = px.histogram(filtered_df, x="Gender", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# 2. Attrition Trends
with tabs[1]:
    st.subheader("Attrition by Business Travel")
    st.markdown("More frequent travel often correlates with higher attrition.")
    travel_chart = px.histogram(filtered_df, x="BusinessTravel", color="Attrition", barmode="group")
    st.plotly_chart(travel_chart, use_container_width=True)

    st.subheader("Attrition vs. OverTime")
    overtime_chart = px.histogram(filtered_df, x="OverTime", color="Attrition", barmode="group")
    st.plotly_chart(overtime_chart, use_container_width=True)

# 3. Departmental Insights
with tabs[2]:
    st.subheader("Attrition by Department and Job Role")
    st.markdown("Compare attrition across departments and roles.")
    dept_chart = px.sunburst(filtered_df, path=["Department", "JobRole", "Attrition"])
    st.plotly_chart(dept_chart, use_container_width=True)

    st.subheader("Attrition by Marital Status")
    marital_chart = px.histogram(filtered_df, x="MaritalStatus", color="Attrition", barmode="group")
    st.plotly_chart(marital_chart, use_container_width=True)

# 4. Satisfaction & Performance
with tabs[3]:
    st.subheader("Job Satisfaction vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="JobSatisfaction", points="all")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Performance Rating Distribution")
    fig = px.histogram(filtered_df, x="PerformanceRating", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# 5. Experience & Tenure
with tabs[4]:
    st.subheader("Years at Company vs Attrition")
    fig = px.box(filtered_df, x="Attrition", y="YearsAtCompany")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Years Since Last Promotion vs Attrition")
    fig = px.violin(filtered_df, x="Attrition", y="YearsSinceLastPromotion", box=True)
    st.plotly_chart(fig, use_container_width=True)

# 6. Compensation Analysis
with tabs[5]:
    st.subheader("Monthly Income Distribution")
    fig = px.histogram(filtered_df, x="MonthlyIncome", color="Attrition", nbins=50, barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Stock Options vs Attrition")
    fig = px.histogram(filtered_df, x="StockOptionLevel", color="Attrition", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# 7. Custom Plots
with tabs[6]:
    st.subheader("Correlation Heatmap")
    st.markdown("Correlation between numeric features.")
    numeric_df = filtered_df.select_dtypes(include='number')
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False, ax=ax)
    st.pyplot(fig)

    st.subheader("Pivot Table: Avg Monthly Income by Department and Attrition")
    pivot = pd.pivot_table(filtered_df, values="MonthlyIncome", index="Department", columns="Attrition", aggfunc="mean")
    st.dataframe(pivot.style.format("${:,.0f}"))
