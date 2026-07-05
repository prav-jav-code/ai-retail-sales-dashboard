import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown(
    """
    <style>
    .main {
        padding-top: 20px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
import os

file_path = os.path.join("cleaned", "Sample - Superstore.csv")

df = pd.read_csv(file_path, encoding="latin1")

# Region filter
regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Category filter
categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Segment filter
segments = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments))
]
# -----------------------------
# Download Data
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export Data")

csv = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    label="Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📊 Retail Sales Analytics Dashboard")
st.caption("Interactive Business Intelligence Dashboard built with Streamlit")

st.markdown("---")

# -----------------------------
# KPI Cards
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("👥 Customers", total_customers)

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

# Sales by Category
with col1:

    st.subheader("📊 Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Sales by Segment
with col2:

    st.subheader("🥧 Sales by Segment")

    segment_sales = (
        filtered_df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        segment_sales,
        values="Sales",
        names="Segment",
        hole=0.45
    )

    st.plotly_chart(fig2, use_container_width=True)
    # -----------------------------
# Monthly Sales Trend
# -----------------------------
st.subheader("📈 Monthly Sales Trend")

# Convert Order Date to datetime
filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

# Create month column
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig3, use_container_width=True)
# -----------------------------
# Profit by Region
# -----------------------------
st.subheader("🌍 Profit by Region")

region_profit = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=".2s",
    title="Profit by Region"
)

st.plotly_chart(fig4, use_container_width=True)
# -----------------------------
# Top 10 Customers
# -----------------------------
st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    color="Sales",
    text_auto=".2s",
    title="Top 10 Customers by Sales"
)

st.plotly_chart(fig5, use_container_width=True)
# -----------------------------
# Top 10 Products
# -----------------------------
st.subheader("📦 Top 10 Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    text_auto=".2s",
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())