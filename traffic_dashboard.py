import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your uploaded file (adjust path if needed)
df = pd.read_csv("traffic_sample_data_clean.csv")

# Preprocess timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day_name()
df['day_night'] = df['hour'].apply(lambda x: 'Night' if x < 6 or x >= 18 else 'Day')

# 1. Line Plot: Vehicle count over time (sample)
px.line(df.head(500), x='timestamp', y='vehicle_count', title='📈 Vehicle Count Over Time').show()

# 2. Pie Chart: Congestion level distribution
px.pie(df, names='congestion_level', title='🟠 Congestion Level Distribution').show()

# 3. Heatmap: Avg vehicle count by hour and day
pivot = df.pivot_table(values='vehicle_count', index='day', columns='hour', aggfunc='mean').fillna(0)
go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Viridis')) \
    .update_layout(title='🔥 Avg Vehicle Count by Hour and Day') \
    .show()

# 4. Box Plot: Speed distribution by congest
px.box(df, x='congestion_level', y='avg_speed', title='📦 Avg Speed by Congestion Level').show()

# 5. Histogram: Vehicle count distribution
px.histogram(df, x='vehicle_count', nbins=50, title='🔢 Vehicle Count Distribution').show()

# 6. Bar Chart: Avg vehicle count by location
avg_by_loc = df.groupby('location')['vehicle_count'].mean().reset_index()
px.bar(avg_by_loc, x='location', y='vehicle_count', title='🏙️ Avg Vehicle Count by Location').show()

# 7. Scatter Plot: Speed vs vehicle count
px.scatter(df.sample(1000), x='avg_speed', y='vehicle_count', color='congestion_level',
           title='🚗 Speed vs Vehicle Count').show()
