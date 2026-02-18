import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

# Configuration
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 1)
DAYS = (END_DATE - START_DATE).days

CHANNELS = {
    'Google Search': {'cpc': (1.5, 4.0), 'cr': (0.05, 0.12), 'aov': (80, 150)}, 
    'Facebook Ads': {'cpc': (0.5, 1.5), 'cr': (0.02, 0.05), 'aov': (40, 90)},   
    'TikTok Ads':   {'cpc': (0.1, 0.4), 'cr': (0.005, 0.02), 'aov': (20, 50)},  
    'Email':        {'cpc': (0.0, 0.0), 'cr': (0.08, 0.15), 'aov': (50, 100)}   
}

CAMPAIGNS = [
    ('CMP-001', 'Google Search', 'Credit Cards Generic'),
    ('CMP-002', 'Google Search', 'Travel Rewards'),
    ('CMP-003', 'Facebook Ads', 'Retargeting - Site Visitors'),
    ('CMP-004', 'Facebook Ads', 'Lookalike - Top Spenders'),
    ('CMP-005', 'TikTok Ads', 'Viral Creative V1'),
    ('CMP-006', 'TikTok Ads', 'Influencer Collab'),
    ('CMP-007', 'Email', 'Weekly Newsletter'),
]

def generate_data():
    data = []
    
    for day in range(DAYS):
        current_date = START_DATE + timedelta(days=day)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Seasonality factor (higher on weekends)
        is_weekend = current_date.weekday() >= 5
        seasonality = 1.2 if is_weekend else 1.0
        
        for camp_id, channel, camp_name in CAMPAIGNS:
            # Base Impressions
            if channel == 'TikTok Ads':
                base = 50000
                variation = random.uniform(0.8, 1.2)
                imps = int(base * variation * seasonality)
            elif channel == 'Email':
                imps = 20000 
            else:
                base = 10000
                variation = random.uniform(0.8, 1.2)
                imps = int(base * variation * seasonality)
            
            # Clicks/CTR
            if channel == 'Email':
                ctr = 0.20 
                clicks = int(imps * ctr * random.uniform(0.8, 1.2))
                cost = 50 
            else:
                params = CHANNELS[channel]
                ctr = random.uniform(0.01, 0.03) 
                clicks = int(imps * ctr)
                cpc = random.uniform(*params['cpc'])
                cost = clicks * cpc
            
            # Conversions
            params = CHANNELS[channel]
            cr = random.uniform(*params['cr'])
            conversions = int(clicks * cr)
            
            # Revenue
            aov = random.uniform(*params['aov'])
            revenue = conversions * aov
            
            data.append({
                'date': date_str,
                'campaign_id': camp_id,
                'campaign_name': camp_name,
                'channel': channel,
                'impressions': imps,
                'clicks': clicks,
                'spend': round(cost, 2),
                'conversions': conversions,
                'revenue': round(revenue, 2)
            })
            
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating marketing data...")
    df = generate_data()
    
    # Save to CSV
    df.to_csv('marketing_data_raw.csv', index=False)
    print(f"Generated {len(df)} rows to marketing_data_raw.csv")
    
    # Load to SQLite
    con = sqlite3.connect('marketing.db')
    df.to_sql('marketing_performance', con, if_exists='replace', index=False)
    
    # Verify
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM marketing_performance")
    count = cursor.fetchone()[0]
    print(f"Loaded {count} rows into SQLite 'marketing.db'")
    con.close()
