import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🚦 Traffic Congestion Analysis Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload cleaned traffic CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocess
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    df['day_night'] = df['hour'].apply(lambda x: 'Night' if x < 6 or x >= 18 else 'Day')

    st.sidebar.header("🔍 Filter Options")
    selected_location = st.sidebar.multiselect("Select Location", options=df['location'].unique(), default=df['location'].unique())
    selected_day_night = st.sidebar.multiselect("Select Time of Day", options=['Day', 'Night'], default=['Day', 'Night'])

    df_filtered = df[(df['location'].isin(selected_location)) & (df['day_night'].isin(selected_day_night))]

    st.markdown("### 📈 Vehicle Count Over Time")
    st.plotly_chart(px.line(df_filtered.head(500), x='timestamp', y='vehicle_count'))

    st.markdown("### 🟠 Congestion Level Distribution")
    st.plotly_chart(px.pie(df_filtered, names='congestion_level', hole=0.4))

    st.markdown("### 🔥 Avg Vehicle Count by Hour and Day")
    pivot = df_filtered.pivot_table(values='vehicle_count', index='day', columns='hour', aggfunc='mean').fillna(0)
    fig_heat = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Viridis'))
    fig_heat.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    st.plotly_chart(fig_heat)

    st.markdown("### 📦 Avg Speed by Congestion Level")
    st.plotly_chart(px.box(df_filtered, x='congestion_level', y='avg_speed', color='congestion_level'))

    st.markdown("### 🔢 Vehicle Count Distribution")
    st.plotly_chart(px.histogram(df_filtered, x='vehicle_count', nbins=50, color='congestion_level'))

    st.markdown("### 🏙️ Avg Vehicle Count by Location")
    avg_by_loc = df_filtered.groupby('location')['vehicle_count'].mean().reset_index()
    st.plotly_chart(px.bar(avg_by_loc, x='location', y='vehicle_count', color='vehicle_count', color_continuous_scale='blues'))

    st.markdown("### 🚗 Speed vs Vehicle Count")
    st.plotly_chart(px.scatter(df_filtered.sample(1000), x='avg_speed', y='vehicle_count', color='congestion_level', size='vehicle_count'))

else:
    st.info("Please upload a CSV file to begin.")
