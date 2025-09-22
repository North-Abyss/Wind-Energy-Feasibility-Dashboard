import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
import altair as alt

# Function: Get coordinates for a city
def get_coords(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    r = requests.get(url, headers={"User-Agent": "WindDashboard/1.0"})
    if r.ok and r.json():
        loc = r.json()[0]
        return float(loc['lat']), float(loc['lon'])
    return None, None

# Function: Fetch Open-Meteo wind data
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

st.set_page_config(page_title="Wind Feasibility Dashboard", layout="wide")
st.title("🌬️ Wind Energy Feasibility Dashboard")

# Input city
city = st.text_input("Enter a City", "Chennai, India")
days = st.slider("Forecast days", 1, 3, 1)

if city:
    lat, lon = get_coords(city)
    if lat:
        # Fetch data
        data = fetch_weather(lat, lon, days)

        # Map
        m = folium.Map(location=[lat, lon], zoom_start=8)
        folium.Marker([lat, lon], tooltip=f"{city}").add_to(m)
        st_data = st_folium(m, width=700, height=500)

        # DataFrame
        df = pd.DataFrame({
            "time": data['hourly']['time'],
            "wind_speed": data['hourly']['wind_speed_10m'],
            "wind_dir": data['hourly']['wind_direction_10m']
        })

        # Show charts
        st.subheader(f"Wind Forecast for {city}")
        chart = alt.Chart(df).mark_line().encode(
            x='time:T', y='wind_speed:Q'
        ).properties(title="Wind Speed (m/s) over Time")
        st.altair_chart(chart, use_container_width=True)

        # Optional: Wind Direction visualization
        st.write("Wind Direction (°):")
        st.line_chart(df.set_index("time")["wind_dir"])
    else:
        st.error("City not found. Try again.")
