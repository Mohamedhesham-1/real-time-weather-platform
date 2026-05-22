
import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🌤 telbs_eh Platform",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0d1117; color: #e6edf3; }
[data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #30363d; }

.metric-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: #58a6ff; }
.metric-label { color: #8b949e; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
.metric-value { color: #e6edf3; font-size: 30px; font-weight: 900; margin: 4px 0; font-family: 'Space Mono', monospace; }
.metric-unit  { color: #58a6ff; font-size: 13px; }

.warning-box {
    background: linear-gradient(135deg, #2d1b1b, #3d2020);
    border: 1px solid #f85149;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 6px 0;
    color: #ffa198;
    font-size: 14px;
}

.outfit-section {
    background: linear-gradient(135deg, #0d1117, #161b22);
    border: 1px solid #238636;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
}
.outfit-title { color: #3fb950; font-size: 16px; font-weight: 700; margin-bottom: 12px; }
.outfit-item  {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 8px 14px; margin: 4px 0;
    font-size: 14px; color: #c9d1d9;
}

.forecast-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 16px; text-align: center;
    transition: border-color 0.2s;
}
.forecast-card:hover { border-color: #58a6ff; }
.forecast-day  { color: #8b949e; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }
.forecast-temp { color: #e6edf3; font-size: 22px; font-weight: 900; font-family: 'Space Mono', monospace; }
.forecast-desc { color: #8b949e; font-size: 11px; margin-top: 4px; }

.section-header {
    font-size: 16px; font-weight: 700; color: #e6edf3;
    border-left: 3px solid #58a6ff; padding-left: 12px;
    margin: 24px 0 12px 0;
}

.stSelectbox label { color: #8b949e !important; font-size: 13px !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DB Connection — reads credentials from st.secrets
# ─────────────────────────────────────────────
def get_conn():
    cfg = st.secrets["mysql"]
    return mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        port=int(cfg.get("port", 3306)),
    )

@st.cache_data(ttl=120)   # refresh every 2 min
def load_current_weather():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT
            cw.*,
            g.city_name,
            g.state_name,
            g.country_code
        FROM OLTP_current_weather cw
        LEFT JOIN gold_city_state_lat_long g
            ON cw.global_cities_id = g.global_id
        ORDER BY cw.dt DESC
    """, conn)
    conn.close()
    return df

@st.cache_data(ttl=3600)  # refresh every hour
def load_forecast():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT
            fw.*,
            g.city_name,
            g.state_name,
            g.country_code
        FROM OLTP_forcast_weather fw
        LEFT JOIN gold_city_state_lat_long g
            ON fw.global_cities_id = g.global_id
        ORDER BY fw.dt ASC
    """, conn)
    conn.close()
    return df

@st.cache_data(ttl=3600)
def load_cities():
    conn = get_conn()
    df = pd.read_sql("""
        SELECT DISTINCT city_name, state_name, country_code
        FROM gold_city_state_lat_long
        ORDER BY city_name
    """, conn)
    conn.close()
    return df

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def weather_emoji(desc):
    if not desc: return "🌤️"
    d = desc.lower()
    if "thunderstorm" in d: return "⛈️"
    if "snow"         in d: return "❄️"
    if "rain"         in d or "drizzle" in d: return "🌧️"
    if "cloud"        in d: return "☁️"
    if "mist"         in d or "fog" in d or "haze" in d: return "🌫️"
    if "clear"        in d: return "☀️"
    return "🌤️"

def temp_level(temp, feels_like):
    eff = (temp + feels_like) / 2
    if eff < 10: return "Freezing"
    if eff < 15: return "Cold"
    if eff < 20: return "Cool"
    if eff < 25: return "Mild"
    if eff < 30: return "Warm"
    return "Hot"

def temp_badge_color(lv):
    return {"Freezing":("#1d4ed8","#93c5fd"),"Cold":("#1e40af","#bfdbfe"),
            "Cool":("#0891b2","#a5f3fc"),"Mild":("#059669","#6ee7b7"),
            "Warm":("#d97706","#fde68a"),"Hot":("#dc2626","#fca5a5")}.get(lv,("#374151","#9ca3af"))

def humidity_note(h):
    if h > 85: return "Suffocating humidity — avoid pure cotton fabrics"
    if h > 70: return "High humidity — choose lightweight, breathable fabrics"
    if h < 30: return "Very dry air — apply moisturizer before heading out"
    return None

def wind_note(w):
    if w > 20: return "Severe winds — a windproof jacket is essential"
    if w > 10: return "Strong winds — wear a wind-resistant outer layer"
    if w > 5:  return "Breezy — keep a light jacket handy"
    return None

def rain_note(desc):
    if not desc: return None
    d = desc.lower()
    if any(x in d for x in ["thunderstorm","heavy rain"]): return "Thunderstorms / heavy rain — large umbrella + waterproof boots"
    if any(x in d for x in ["rain","drizzle","shower"]):   return "Rain likely — carry an umbrella or waterproof jacket"
    if "cloud" in d: return "Overcast — rain is possible, umbrella recommended"
    return None

# ─────────────────────────────────────────────
# Outfit Recommender
# ─────────────────────────────────────────────
def get_outfit(temp, feels_like, humidity, wind_speed, weather_desc, gender, occasion):
    lv     = temp_level(temp, feels_like)
    d      = (weather_desc or "").lower()
    rainy  = any(x in d for x in ["rain","drizzle","shower","thunderstorm"])
    windy  = wind_speed > 10
    female = gender == "Female"

    if occasion == "Sport":
        if lv in ["Freezing","Cold"]:
            return {"tops":["Thermal base layer","Sports hoodie"],"bottoms":["Thermal tights","Joggers over tights"],"shoes":"Closed-toe running shoes","accessories":["Sports gloves","Running headband"]}
        if lv in ["Cool","Mild"]:
            return {"tops":["Sports t-shirt"],"bottoms":["Athletic shorts" if lv=="Mild" else "Joggers"],"shoes":"Lightweight running shoes","accessories":[]}
        return {"tops":["Ultra-light sports tee"],"bottoms":["Light athletic shorts"],"shoes":"Light sneakers or sport sandals","accessories":["Cap for sun protection"]}

    if occasion == "Work":
        if lv in ["Freezing","Cold"]:
            return {"tops":["Dress shirt","Suit jacket or blazer","Overcoat if very cold"],"bottoms":["Formal trousers"],"shoes":"Leather shoes or formal boots","accessories":["Tie or scarf if needed"]}
        if lv in ["Cool","Mild"]:
            return {"tops":["Smart-casual shirt","Light blazer"],"bottoms":["Chinos or formal trousers"],"shoes":"Loafers or light leather shoes","accessories":["Watch","Leather belt"]}
        return {"tops":["Light cotton button-up" if not female else "Light blouse"],"bottoms":["Light-coloured chinos"],"shoes":"Loafers or light shoes","accessories":["Watch"]}

    # Casual / Outing
    if lv == "Freezing":
        return {"tops":["Thermal undershirt","Heavy sweatshirt","Parka or heavy coat"],"bottoms":["Thick jeans or wool trousers"],"shoes":"Heavy leather boots","accessories":["Wool scarf","Beanie","Gloves"]}
    if lv == "Cold":
        acc = ["Light scarf"] + (["Umbrella"] if rainy else [])
        return {"tops":["T-shirt","Hoodie or sweatshirt"] + (["Windproof jacket"] if windy else []),"bottoms":["Jeans"],"shoes":"Closed sneakers or light boots","accessories":acc}
    if lv == "Cool":
        return {"tops":["T-shirt","Hoodie or overshirt"],"bottoms":["Jeans"],"shoes":"Sneakers","accessories":["Umbrella"] if rainy else []}
    if lv == "Mild":
        return {"tops":["Light t-shirt" if not female else "T-shirt or light blouse"],"bottoms":["Jeans or chinos"],"shoes":"Sneakers or casual shoes","accessories":["Umbrella"] if rainy else []}
    if lv == "Warm":
        return {"tops":["Light t-shirt"],"bottoms":["Shorts or light jeans"],"shoes":"Light sneakers or sandals","accessories":["Sunglasses","Cap"]}
    return {"tops":["Ultra-light cotton tee" if not female else "Light tee or summer dress"],"bottoms":["Shorts"],"shoes":"Sandals or flip-flops","accessories":["Sunglasses","Cap or hat","Sunscreen — essential"]}

def mcard(label, value, unit=""):
    return f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}<span class="metric-unit"> {unit}</span></div></div>'

# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
try:
    current_df = load_current_weather()
    forecast_df = load_forecast()
    cities_df   = load_cities()
    db_ok = True
except Exception as e:
    db_ok = False
    db_error = str(e)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px 0;'>
        <div style='font-size:42px;'>🌤️</div>
        <div style='font-size:20px;font-weight:900;color:#e6edf3;'>telbs_eh Platform</div>
        <div style='font-size:12px;color:#8b949e;margin-top:4px;'>Powered by Airflow + MySQL</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    if db_ok and not cities_df.empty:
        city_options = sorted(cities_df["city_name"].dropna().unique().tolist())
        selected_city = st.selectbox("🏙️ Select City", city_options)
    else:
        selected_city = None
        st.warning("No cities found in database.")

    st.markdown("**⚙️ Outfit Preferences**")
    gender   = st.selectbox("Gender",   ["Male", "Female"])
    occasion = st.selectbox("Occasion", ["Casual", "Work", "Sport", "Outing"])

    st.divider()
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<div style='color:#8b949e;font-size:12px;text-align:center;'>Current data refreshes every 2 min<br>Forecast refreshes every hour</div>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DB Error State
# ─────────────────────────────────────────────
if not db_ok:
    st.error(f"❌ Could not connect to the database: **{db_error}**")
    st.markdown("""
    Make sure your `.streamlit/secrets.toml` file exists and contains:
    ```toml
    [mysql]
    host     = "localhost"
    user     = "root"
    password = "password"
    database = "telbs_ehh"
    port     = 3306
    ```
    """)
    st.stop()

if selected_city is None:
    st.info("No data in the database yet. Run your Airflow DAG first to populate the tables.")
    st.stop()

# ─────────────────────────────────────────────
# Filter to selected city
# ─────────────────────────────────────────────
city_current  = current_df[current_df["city_name"] == selected_city]
city_forecast = forecast_df[forecast_df["city_name"] == selected_city]

if city_current.empty:
    st.warning(f"No current weather data for **{selected_city}** yet. Wait for Airflow to run.")
    st.stop()

# Latest row for current weather
row = city_current.iloc[0]
temp       = float(row["temp"])
feels_like = float(row["feels_like"])
humidity   = int(row["humidity"])
wind_speed = float(row["wind_speed"])
desc       = str(row.get("weather_desc", ""))
visibility = float(row["visibility"]) / 1000 if row.get("visibility") else 0
sunrise_dt = row.get("sunrise")
sunset_dt  = row.get("sunset")
country    = str(row.get("country_code", ""))
state      = str(row.get("state_name", ""))
last_upd   = row.get("dt", "—")
emoji      = weather_emoji(desc)
lv         = temp_level(temp, feels_like)
bg, fg     = temp_badge_color(lv)

# ── City Header ──
st.markdown(f"""
<div style='background:linear-gradient(135deg,#1c2128,#21262d);border:1px solid #30363d;border-radius:20px;padding:28px 32px;margin-bottom:24px;'>
  <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;'>
    <div>
      <div style='font-size:34px;font-weight:900;color:#e6edf3;'>{emoji} {selected_city}, {state}, {country}</div>
      <div style='font-size:14px;color:#8b949e;margin-top:6px;'>Last updated by Airflow: {last_upd} &nbsp;•&nbsp; {desc.title()}</div>
      <div style='margin-top:10px;'>
        <span style='background:{bg};color:{fg};padding:4px 14px;border-radius:20px;font-size:13px;font-weight:700;'>{lv}</span>
      </div>
    </div>
    <div style='text-align:center;'>
      <div style='font-size:80px;font-weight:900;color:#58a6ff;font-family:"Space Mono",monospace;line-height:1;'>{temp:.0f}°</div>
      <div style='color:#8b949e;font-size:14px;'>Feels like {feels_like:.0f}°C</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ──
st.markdown('<div class="section-header">📊 Current Conditions</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(mcard("💧 Humidity",   f"{humidity}",       "%"),    unsafe_allow_html=True)
c2.markdown(mcard("💨 Wind",       f"{wind_speed:.1f}", "m/s"),  unsafe_allow_html=True)
c3.markdown(mcard("👁️ Visibility", f"{visibility:.1f}", "km"),   unsafe_allow_html=True)
if sunrise_dt:
    c4.markdown(mcard("🌅 Sunrise", pd.Timestamp(sunrise_dt).strftime("%I:%M %p"), ""), unsafe_allow_html=True)
if sunset_dt:
    c5.markdown(mcard("🌇 Sunset",  pd.Timestamp(sunset_dt).strftime("%I:%M %p"),  ""), unsafe_allow_html=True)

# ── Warnings ──
warns = [w for w in [humidity_note(humidity), wind_note(wind_speed), rain_note(desc)] if w]
if warns:
    st.markdown('<div class="section-header">⚠️ Weather Alerts</div>', unsafe_allow_html=True)
    for w in warns:
        st.markdown(f'<div class="warning-box">⚠️ {w}</div>', unsafe_allow_html=True)

# ── Outfit + Forecast ──
col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown('<div class="section-header">👗 Outfit Recommendation</div>', unsafe_allow_html=True)
    outfit = get_outfit(temp, feels_like, humidity, wind_speed, desc, gender, occasion)
    st.markdown(f'<div class="outfit-section"><div class="outfit-title">🎯 {occasion} &nbsp;•&nbsp; {gender} &nbsp;•&nbsp; {lv}</div>', unsafe_allow_html=True)
    if outfit.get("tops"):
        st.markdown("**Upper layers:**")
        for item in outfit["tops"]:
            st.markdown(f'<div class="outfit-item">👕 {item}</div>', unsafe_allow_html=True)
    if outfit.get("bottoms"):
        st.markdown("**Bottoms:**")
        for item in outfit["bottoms"]:
            st.markdown(f'<div class="outfit-item">👖 {item}</div>', unsafe_allow_html=True)
    st.markdown("**Footwear:**")
    st.markdown(f'<div class="outfit-item">👟 {outfit["shoes"]}</div>', unsafe_allow_html=True)
    if outfit.get("accessories"):
        st.markdown("**Accessories:**")
        for acc in outfit["accessories"]:
            st.markdown(f'<div class="outfit-item">🎒 {acc}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="section-header">📅 5-Day Forecast</div>', unsafe_allow_html=True)
    if city_forecast.empty:
        st.info("No forecast data available yet for this city.")
    else:
        city_forecast = city_forecast.copy()
        city_forecast["dt"] = pd.to_datetime(city_forecast["dt"])
        city_forecast["date"] = city_forecast["dt"].dt.date
        daily = city_forecast.groupby("date").agg(
            avg_temp=("temp", "mean"),
            max_temp=("temp", "max"),
            min_temp=("temp", "min"),
            desc=("weather_desc", lambda x: x.mode()[0] if not x.empty else "")
        ).reset_index().head(6)

        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        cols_f = st.columns(len(daily))
        today  = datetime.today().date()

        for i, r2 in enumerate(daily.itertuples()):
            label  = "Today" if r2.date == today else day_names[r2.date.weekday()]
            border = "border-color:#58a6ff;" if r2.date == today else ""
            cols_f[i].markdown(f"""
            <div class="forecast-card" style='{border}'>
                <div class="forecast-day">{label}</div>
                <div style='font-size:24px;margin:6px 0;'>{weather_emoji(r2.desc)}</div>
                <div class="forecast-temp">{r2.avg_temp:.0f}°</div>
                <div style='color:#3fb950;font-size:11px;'>↑{r2.max_temp:.0f}° ↓{r2.min_temp:.0f}°</div>
                <div class="forecast-desc">{str(r2.desc)[:14]}</div>
            </div>""", unsafe_allow_html=True)

# ── Hourly Chart (next 24h from forecast) ──
if not city_forecast.empty:
    st.markdown('<div class="section-header">📈 Temperature — Next 24 Hours</div>', unsafe_allow_html=True)
    now   = pd.Timestamp.now()
    next24 = city_forecast[city_forecast["dt"] >= now].head(8).copy()
    if not next24.empty:
        next24["Time"] = next24["dt"].dt.strftime("%I %p")
        chart_df = next24.set_index("Time")[["temp","feels_like"]].rename(
            columns={"temp": "Temperature", "feels_like": "Feels Like"})
        st.line_chart(chart_df, use_container_width=True, height=220)

# ── Historical Table ──
st.markdown('<div class="section-header">🗃️ Recent Readings (from DB)</div>', unsafe_allow_html=True)
hist = city_current[["dt","temp","feels_like","humidity","wind_speed","weather_desc"]].head(10).copy()
hist.columns = ["Timestamp","Temp (°C)","Feels Like (°C)","Humidity (%)","Wind (m/s)","Condition"]
st.dataframe(hist, use_container_width=True, hide_index=True)

# ── Footer ──
st.markdown("""
<div style='text-align:center;color:#484f58;font-size:12px;margin-top:32px;padding:16px;border-top:1px solid #21262d;'>
    Real-Time Weather Platform &nbsp;•&nbsp; Data by Airflow + OpenWeather &nbsp;•&nbsp; Visualized with Streamlit
</div>""", unsafe_allow_html=True)
