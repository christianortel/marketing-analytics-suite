import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Deep Dive | Launch Potato", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect('marketing.db')
    df = pd.read_sql_query("SELECT * FROM marketing_performance", conn)
    conn.close()
    return df

df = load_data()

st.title("🔬 Campaign Deep Dive")
st.markdown("Analyze campaign efficiency and outliers.")

# Scatter Plot: Spend vs Revenue (Efficiency Frontier)
st.subheader("Efficiency Frontier: Spend vs. Revenue")
st.markdown("Identify high-performing campaigns (Top Left) vs. inefficient ones (Bottom Right).")

# Aggregate by campaign
camp_agg = df.groupby(['campaign_name', 'channel']).agg({
    'spend': 'sum',
    'revenue': 'sum',
    'conversions': 'sum',
    'impressions': 'sum'
}).reset_index()

camp_agg['ROAS'] = camp_agg['revenue'] / camp_agg['spend']
camp_agg['CPA'] = camp_agg['spend'] / camp_agg['conversions']

fig = px.scatter(camp_agg, x="spend", y="revenue", 
                 size="conversions", color="channel",
                 hover_name="campaign_name",
                 text="campaign_name",
                 title="Campaign Performance (Size = Conversions)",
                 template="plotly_dark")
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top ROAS Campaigns")
    st.dataframe(
        camp_agg.sort_values('ROAS', ascending=False)[['campaign_name', 'channel', 'ROAS']].head(5)
        .style.format({'ROAS': '{:.2f}x'}),
        use_container_width=True
    )

with col2:
    st.subheader("Highest CPA (Needs Optimization)")
    st.dataframe(
        camp_agg.sort_values('CPA', ascending=False)[['campaign_name', 'channel', 'CPA']].head(5)
        .style.format({'CPA': '${:.2f}'}),
        use_container_width=True
    )
