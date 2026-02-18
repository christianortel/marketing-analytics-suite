import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="SQL Lab | Launch Potato", layout="wide")

st.title("💻 SQL Inspector (Ad-Hoc Analysis)")
st.markdown("Use this workspace to run raw SQL queries against the `marketing_performance` table.")

# Connection
def get_connection():
    return sqlite3.connect('marketing.db')

# Schema View
with st.expander("View Schema", expanded=True):
    conn = get_connection()
    schema = pd.read_sql("PRAGMA table_info(marketing_performance)", conn)
    st.dataframe(schema)
    conn.close()

# Query Editor
tab1, tab2 = st.tabs(["🔒 SQL Editor", "🔎 Data Explorer"])

with tab1:
    default_query = """
SELECT 
    channel, 
    SUM(spend) as total_spend,
    SUM(revenue) as total_revenue,
    SUM(revenue) / SUM(spend) as ROAS
FROM marketing_performance
GROUP BY channel
ORDER BY ROAS DESC
"""
    query = st.text_area("SQL Query", default_query, height=200)
    if st.button("Run Query"):
        try:
            conn = get_connection()
            df = pd.read_sql_query(query, conn)
            st.success(f"Returned {len(df)} rows")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {e}")
        finally:
            conn.close()

with tab2:
    st.markdown("### Raw Data Browser")
    # Load all data (it's small enough)
    conn = get_connection()
    full_df = pd.read_sql_query("SELECT * FROM marketing_performance", conn)
    conn.close()
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sel_channel = st.multiselect("Filter Channel", full_df['channel'].unique())
    with col_f2:
        sel_campaign = st.multiselect("Filter Campaign", full_df['campaign_name'].unique())
    
    if sel_channel:
        full_df = full_df[full_df['channel'].isin(sel_channel)]
    if sel_campaign:
        full_df = full_df[full_df['campaign_name'].isin(sel_campaign)]
        
    st.dataframe(full_df, use_container_width=True)
    st.caption(f"Showing {len(full_df)} rows")
