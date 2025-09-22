import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta
import math

# Function: Get coordinates for a city
def get_coords(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    r = requests.get(url, headers={"User-Agent": "WindDashboard/1.0"})
    if r.ok and r.json():
        loc = r.json()[0]
        return float(loc['lat']), float(loc['lon'])
    return None, None

# Function: Fetch Open-Meteo forecast data
def fetch_weather(lat, lon, days=1):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "forecast_days": days,
        "timezone": "auto"
    }
    r = requests.get(url, params=params)
    return r.json() if r.ok else None

# Function: Fetch past data (up to 10 months back)
def fetch_past_weather(lat, lon, days=10):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "hourly": "wind_speed_10m,wind_direction_10m",
        "timezone": "auto"
    }
    r = requests.get(url, params=params)
    return r.json() if r.ok else None

# Wind direction as compass text
def compass_dir(degree):
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    ix = round(degree / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

st.set_page_config(page_title="Wind Feasibility Dashboard", layout="wide")
st.title("🌬️ Wind Energy Feasibility Dashboard")

# Input city
city = st.text_input("Enter a City", "Chennai, India")
forecast_days = st.selectbox("Forecast Days", [1, 2, 3, 4, 5], index=0)

if city:
    lat, lon = get_coords(city)
    if lat:
        # Fetch forecast
        data = fetch_weather(lat, lon, forecast_days)

        # Map
        m = folium.Map(location=[lat, lon], zoom_start=8)
        folium.Marker([lat, lon], tooltip=f"{city}").add_to(m)
        st_data = st_folium(m, width=700, height=400)

        # DataFrame
        df = pd.DataFrame({
            "time": data['hourly']['time'],
            "wind_speed": data['hourly']['wind_speed_10m'],
            "wind_dir": data['hourly']['wind_direction_10m']
        })

        # Average wind speed
        avg_speed = np.mean(df["wind_speed"])
        st.metric(label="💨 Average Wind Speed (m/s)", value=f"{avg_speed:.2f}")

        # Show compass for last data point
        last_dir = df["wind_dir"].iloc[-1]
        st.write(f"🧭 Current Wind Direction: **{compass_dir(last_dir)} ({last_dir:.0f}°)**")

        # Interactive Altair Chart
        st.subheader(f"Wind Forecast for {city}")
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('time:T', title='Time'),
            y=alt.Y('wind_speed:Q', title='Wind Speed (m/s)'),
            tooltip=['time:T', 'wind_speed:Q', 'wind_dir:Q']
        ).interactive().properties(title="Wind Speed (m/s) over Time")
        st.altair_chart(chart, use_container_width=True)

        # Optional: Wind Direction chart
        st.write("Wind Direction (°):")
        chart2 = alt.Chart(df).mark_line(point=True).encode(
            x='time:T', y='wind_dir:Q', tooltip=['time:T','wind_dir:Q']
        ).interactive().properties(title="Wind Direction (°) over Time")
        st.altair_chart(chart2, use_container_width=True)

        # Download past data
        st.subheader("📥 Download Past Wind Data")
        past_range = st.selectbox("Select past data range",
                                  ["10 days", "1 month", "3 months", "6 months", "10 months"])
        if st.button("Fetch Past Data"):
            days_lookup = {"10 days":10, "1 month":30, "3 months":90,
                           "6 months":180, "10 months":300}
            past = fetch_past_weather(lat, lon, days_lookup[past_range])
            past_df = pd.DataFrame({
                "time": past['hourly']['time'],
                "wind_speed": past['hourly']['wind_speed_10m'],
                "wind_dir": past['hourly']['wind_direction_10m']
            })
            csv = past_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"Download past {past_range} wind data as CSV",
                data=csv,
                file_name=f"{city.replace(' ','_')}_wind_history.csv",
                mime="text/csv",
            )
    else:
        st.error("City not found. Try again.")
