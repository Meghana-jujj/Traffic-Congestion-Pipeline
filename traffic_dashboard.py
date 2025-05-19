import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Traffic Congestion Dashboard", layout="wide")
st.title("🚦 Real-Time Traffic Congestion Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("📁 Upload traffic_sample_data_clean.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_night'] = df['hour'].apply(lambda x: 'Night' if x < 6 or x >= 18 else 'Day')

    st.success("✅ Data loaded successfully!")
    st.write("### Sample Data", df.head())

    # Congestion Level Pie Chart
    st.subheader("🚗 Congestion Level Distribution")
    pie_fig = px.pie(df, names="congestion_level", title="Overall Congestion Levels", hole=0.4)
    st.plotly_chart(pie_fig, use_container_width=True)

    # Average Speed Line Chart
    st.subheader("📈 Average Speed Over Time")
    speed_fig = px.line(df.sort_values("timestamp").head(500), x="timestamp", y="avg_speed", title="Average Speed Over Time")
    st.plotly_chart(speed_fig, use_container_width=True)

    # Vehicle Count Box Plot by Location
    st.subheader("📦 Vehicle Count Distribution by Location")
    box_fig = px.box(df, x="location", y="vehicle_count", title="Vehicle Count per Location")
    st.plotly_chart(box_fig, use_container_width=True)

    # Heatmap: Hour vs Location
    st.subheader("🌡️ Heatmap of Traffic by Hour and Location")
    heatmap_data = df.groupby(['hour', 'location']).size().reset_index(name='count')
    heatmap_fig = px.density_heatmap(
        heatmap_data,
        x='hour', y='location', z='count',
        title="Traffic Volume Heatmap (Hour vs Location)",
        nbinsx=24, color_continuous_scale='Viridis'
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

    # Day vs Night Trend
    st.subheader("🌞 Day vs 🌙 Night Traffic Trends")
    dn_fig = px.bar(
        df.groupby('day_night')['vehicle_count'].mean().reset_index(),
        x='day_night', y='vehicle_count',
        title="Average Vehicle Count: Day vs Night"
    )
    st.plotly_chart(dn_fig, use_container_width=True)

else:
    st.warning("📂 Please upload the `traffic_sample_data_clean.csv` file to see the dashboard.")

