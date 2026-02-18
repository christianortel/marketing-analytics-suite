import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Setup
st.set_page_config(page_title="Launch Potato Analytics", layout="wide")

# Theme
st.markdown("""
<style>
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Data Connection
@st.cache_data
def load_data():
    conn = sqlite3.connect('marketing.db')
    try:
        df = pd.read_sql_query("SELECT * FROM marketing_performance", conn)
        return df
    finally:
        conn.close()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading database: {e}")
    st.stop()

# Sidebar
st.sidebar.title("🔍 Filters")
channels = st.sidebar.multiselect("Select Channels", df['channel'].unique(), default=df['channel'].unique())

if channels:
    filtered_df = df[df['channel'].isin(channels)]
else:
    filtered_df = df

st.title("🥔 Launch Potato Marketing Intelligence")
st.markdown("### Executive Summary (Q1 2025)")

# Top Level Metrics
total_spend = filtered_df['spend'].sum()
total_revenue = filtered_df['revenue'].sum()
total_conversions = filtered_df['conversions'].sum()
roas = total_revenue / total_spend if total_spend > 0 else 0
cpa = total_spend / total_conversions if total_conversions > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend", f"${total_spend:,.0f}")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Blended ROAS", f"{roas:.2f}x", delta=f"{(roas-2.5):.2f} vs Target")
col4.metric("CPA", f"${cpa:.2f}", delta_color="inverse", delta=f"{(cpa-45):.2f} vs Target")

st.markdown("---")

# Trend Analysis
col_chart, col_table = st.columns([2, 1])

with col_chart:
    st.subheader("Daily Revenue Trend")
    daily = filtered_df.groupby('date')[['spend', 'revenue']].sum().reset_index()
    fig = px.line(daily, x='date', y=['revenue', 'spend'], 
                  color_discrete_map={'revenue': '#4CAF50', 'spend': '#FF5252'},
                  title="Revenue vs Ad Spend")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.subheader("Channel Performance")
    channel_perf = filtered_df.groupby('channel').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    channel_perf['ROAS'] = channel_perf['revenue'] / channel_perf['spend']
    channel_perf['CPA'] = channel_perf['spend'] / channel_perf['conversions']
    
    st.dataframe(
        channel_perf.style.format({
            "spend": "${:,.0f}", 
            "revenue": "${:,.0f}", 
            "ROAS": "{:.2f}x",
            "CPA": "${:.2f}"
        }).background_gradient(subset=['ROAS'], cmap='Greens'),
        use_container_width=True
    )

st.markdown("---")
st.subheader("💡 Budget Allocator (Simulator)")

sim_col1, sim_col2 = st.columns([1, 2])

with sim_col1:
    st.markdown("#### Adjust Monthly Budget")
    google_budget = st.slider("Google Search Budget", 0, 50000, 15000, step=1000)
    fb_budget = st.slider("Facebook Ads Budget", 0, 50000, 10000, step=1000)
    tiktok_budget = st.slider("TikTok Ads Budget", 0, 50000, 5000, step=1000)

with sim_col2:
    st.markdown("#### Predicted Outcome")
    
    # Simple linear projection model based on historical channel ROAS
    # In a real app, this would use marginal ROAS curves (diminishing returns)
    roas_map = channel_perf.set_index('channel')['ROAS'].to_dict()
    
    pred_rev_google = google_budget * roas_map.get('Google Search', 0)
    pred_rev_fb = fb_budget * roas_map.get('Facebook Ads', 0)
    pred_rev_tiktok = tiktok_budget * roas_map.get('TikTok Ads', 0)
    
    total_pred_rev = pred_rev_google + pred_rev_fb + pred_rev_tiktok
    total_new_budget = google_budget + fb_budget + tiktok_budget
    current_rev_est = (15000 * roas_map.get('Google Search', 0)) + \
                      (10000 * roas_map.get('Facebook Ads', 0)) + \
                      (5000 * roas_map.get('TikTok Ads', 0))
    
    delta_rev = total_pred_rev - current_rev_est
    
    st.metric("Projected Monthly Revenue", f"${total_pred_rev:,.0f}", 
             delta=f"${delta_rev:,.0f} vs Baseline")
    
    st.progress(min(1.0, total_pred_rev / 200000))
    st.caption("Revenue Goal Progress ($200k)")

st.info("Recommendation: Shift budget from **Facebook Ads** (Lower ROAS) to **Google Search** (Higher ROAS) to maximize return.")
