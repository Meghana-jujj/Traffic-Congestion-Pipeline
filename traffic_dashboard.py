import streamlit as st
import pandas as pd
import plotly.express as px

# --- App Title ---
st.set_page_config(page_title="🚦 Traffic Data Dashboard", layout="wide")
st.title("🚦 Real-Time Traffic Data Analysis Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your cleaned traffic CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_period'] = df['hour'].apply(lambda x: 'Night' if (x < 6 or x >= 18) else 'Day')

    # --- KPI Section ---
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Average Speed", f"{df['avg_speed'].mean():.2f} km/h")
    col3.metric("Total Vehicles", f"{df['vehicle_count'].sum():,}")

    st.markdown("---")

    # --- Filter Section ---
    st.sidebar.header("🔍 Filters")
    locations = st.sidebar.multiselect("Select Location(s)", options=df['location'].unique(), default=df['location'].unique())
    congestion_levels = st.sidebar.multiselect("Select Congestion Level(s)", options=df['congestion_level'].unique(), default=df['congestion_level'].unique())

    filtered_df = df[(df['location'].isin(locations)) & (df['congestion_level'].isin(congestion_levels))]

    # --- Charts Section ---
    st.subheader("📈 Traffic Trends")

    fig1 = px.line(filtered_df, x="timestamp", y="vehicle_count", color="location", title="📌 Vehicle Count Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(filtered_df, x="hour", y="vehicle_count", color="day_period", title="🌓 Traffic Pattern: Day vs Night", barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(filtered_df, x="avg_speed", y="vehicle_count", color="congestion_level", size="vehicle_count", hover_data=["location"], title="🚗 Speed vs Vehicle Count")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.pie(filtered_df, names='congestion_level', title='🥧 Congestion Level Distribution')
    st.plotly_chart(fig4, use_container_width=True)

    # --- Save Filtered Data ---
    st.subheader("📥 Download Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", data=csv, file_name='filtered_traffic_data.csv', mime='text/csv')

else:
    st.info("Please upload a cleaned traffic data CSV file to begin.")
