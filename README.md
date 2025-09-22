# Wind Energy Feasibility Dashboard 🌬️

An interactive **Streamlit dashboard** that estimates wind energy feasibility for any city, based on real-time and historical wind data from the **Open-Meteo API**.

Live Demo hosted on Streamlit:
🔗 [wind-energy-feasibility-dashboard.streamlit.app](https://wind-energy-feasibility-dashboard.streamlit.app/)

---

## 📌 Features & Highlights

* **City-based search input** with integrated geocoding
* **Interactive map** view using OpenStreetMap (via `folium`)
* **Hourly wind speed (m/s)** and **wind direction (°)** visualization
* **Average wind speed metric** displayed prominently
* **Compass-style indicator** for current wind direction
* **Interactive Altair charts**: hover to view speed & direction values
* **Downloadable historical data** covering the past 10 days up to 10 months

---

## 🧰 Tech Stack

* **Streamlit** — for building the web interface
* **Open-Meteo API** — for fetching wind forecast and archive data
* **Nominatim API** — to geocode city names from user input
* **Folium + `streamlit-folium`** — to render interactive maps
* **Altair + pandas** — for plotting time-series data

---

## 🚀 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/wind-energy-feasibility-dashboard.git
   cd wind-energy-feasibility-dashboard
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

   Open your browser at `http://localhost:8501` to view the dashboard.

---

## 🧭 How It Works

1. **Enter a city name** → the app uses Nominatim API to get coordinates
2. **Forecast**: retrieves forecasted wind speed & direction for up to 5 days
3. **Visualization**:

   * Pinpoint map with city marker & zoom view
   * Time-series charts and metrics for wind speed and direction
   * Compass indicator for current wind direction
   * Big-font average wind speed statistic
4. **Historical Data**:

   * Select range (10 days to 10 months)
   * Fetch and download hourly wind data as CSV for offline analysis

---

## 🧪 Why This Matters

Wind resource assessment supports renewable energy planning — informing decisions on turbine siting, expected power output, and overall feasibility. This tool offers a lightweight, transparent, and interactive way to understand wind potential using open data sources — all without needing proprietary data or paid services.

---

## 📚 Inspired By

This dashboard aligns closely with other Streamlit-based wind resource projects that emphasize modern data workflows and interactivity. For example: the **Wind Energy Dashboard** GitHub project by *gbabeleda* demonstrates the integration of Streamlit with data warehouse technologies for wind resource analysis ([GitHub][1]).

---

## 🛠️ Future Enhancements (Suggestions)

* Add **wind rose diagrams** to show direction-frequency distributions
* Compute basic **energy output estimates** using a sample turbine (power ∝ wind speed³)
* Model **Weibull distribution** and wind power frequency histograms
* Provide a **dark mode theme** or mobile-responsive layouts
* Deploy with **GitHub Actions** or integrate with a CI/CD pipeline for updates

---

### 📩 Contributing & Support

Contributions are welcome! Whether it’s a bug fix, UI improvement, or a new feature like energy yield estimation — feel free to open issues or pull requests.

I hope this tool becomes a helpful part of your green energy toolkit!

