import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

st.set_page_config(layout="wide")
st.title("🚦 Traffic Congestion Analysis Dashboard")

uploaded_file = st.file_uploader("Upload cleaned traffic CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocess
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day_name()
    df['day_night'] = df['hour'].apply(lambda x: 'Night' if x < 6 or x >= 18 else 'Day')

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    selected_location = st.sidebar.multiselect("Select Location", options=df['location'].unique(), default=df['location'].unique())
    selected_day_night = st.sidebar.multiselect("Select Time of Day", options=['Day', 'Night'], default=['Day', 'Night'])
    selected_congestion = st.sidebar.multiselect("Select Congestion Level", options=df['congestion_level'].unique(), default=df['congestion_level'].unique())
    selected_days = st.sidebar.multiselect("Select Days of Week", options=df['day'].unique(), default=df['day'].unique())

    # Filter dataframe
    df_filtered = df[
        (df['location'].isin(selected_location)) &
        (df['day_night'].isin(selected_day_night)) &
        (df['congestion_level'].isin(selected_congestion)) &
        (df['day'].isin(selected_days))
    ]

    # Geocoding part (same as before)
    location_coords = {
        'I-94 Highway': {'lat': 44.9778, 'lon': -93.2650},
        'I-35W Highway': {'lat': 44.9510, 'lon': -93.0890},
        'I-494 Highway': {'lat': 44.8704, 'lon': -93.3127},
    }

    geolocator = Nominatim(user_agent="traffic_dashboard")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    def get_coords(location):
        if location in location_coords:
            return location_coords[location]['lat'], location_coords[location]['lon']
        try:
            loc = geocode(location + ", Minnesota, USA")
            if loc:
                return loc.latitude, loc.longitude
        except:
            return None, None
        return None, None

    coords = df_filtered['location'].apply(get_coords)
    df_filtered['lat'] = coords.apply(lambda x: x[0])
    df_filtered['lon'] = coords.apply(lambda x: x[1])
    df_map = df_filtered.dropna(subset=['lat', 'lon']).copy()

    # View toggle
    view_option = st.sidebar.radio("Select View", ("Charts View", "Map View"))

    px.set_mapbox_access_token("YOUR_MAPBOX_TOKEN")

    if view_option == "Map View":
        st.markdown("### 🗺️ Traffic Congestion Map")
        fig_map = px.scatter_mapbox(
            df_map.head(1000),
            lat="lat",
            lon="lon",
            color="congestion_level",
            size="vehicle_count",
            hover_name="location",
            hover_data=["avg_speed", "timestamp"],
            zoom=9,
            height=600,
            title="Traffic Congestion Map"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    else:
        st.markdown("### 📈 Vehicle Count Over Time (Animated by Hour)")
        # Animation: frame by 'hour' to show changes throughout the day
        df_anim = df_filtered.sort_values('timestamp')
        fig_anim = px.line(df_anim, x='timestamp', y='vehicle_count', color='location',
                           animation_frame=df_anim['hour'], range_y=[0, df_filtered['vehicle_count'].max() + 10])
        st.plotly_chart(fig_anim)

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
        st.plotly_chart(px.scatter(df_filtered.sample(min(1000, len(df_filtered))), x='avg_speed', y='vehicle_count', color='congestion_level', size='vehicle_count'))

else:
    st.info("Please upload a CSV file to begin.")
