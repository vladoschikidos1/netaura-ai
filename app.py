import html
import streamlit as st

from weather import get_weather, get_weather_data
from ai_chat import ask_gemini


APP_NAME = "NetAura AI"


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌐",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #073b5a 0%, #07111f 42%, #04070d 100%);
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0b2338 100%);
    border-right: 1px solid rgba(0, 174, 239, 0.25);
}

.hero {
    background: linear-gradient(135deg, #005073 0%, #0078a8 45%, #00a9e0 100%);
    padding: 34px;
    border-radius: 28px;
    color: white;
    text-align: center;
    box-shadow: 0 16px 45px rgba(0, 169, 224, 0.28);
    margin-bottom: 26px;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.95;
}

.panel-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    margin-bottom: 18px;
    backdrop-filter: blur(14px);
}

.panel-card h3 {
    color: #ffffff;
    margin-top: 0;
    margin-bottom: 8px;
    font-size: 23px;
}

.panel-card p {
    color: #b8d8e8;
    margin-bottom: 0;
    font-size: 15px;
}

.weather-main-card {
    background: linear-gradient(160deg, #1594d2 0%, #0b72ad 48%, #0a3d68 100%);
    color: white;
    padding: 30px;
    border-radius: 30px;
    box-shadow: 0 16px 40px rgba(0, 169, 224, 0.25);
    margin-top: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.weather-location {
    font-size: 24px;
    font-weight: 850;
    margin-bottom: 6px;
}

.weather-condition {
    font-size: 17px;
    color: #d9f3ff;
    margin-bottom: 20px;
}

.weather-temp {
    font-size: 74px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 8px;
}

.weather-feels {
    font-size: 17px;
    color: #d9f3ff;
}

.weather-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-top: 14px;
}

.weather-tile {
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 22px;
    padding: 20px;
    min-height: 130px;
    color: white;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.20);
}

.tile-label {
    color: #aee6ff;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.tile-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: 850;
    margin-bottom: 6px;
}

.tile-note {
    color: #c8e8f5;
    font-size: 14px;
    line-height: 1.35;
}

.stTextInput input {
    border-radius: 16px;
}

.stButton button {
    border-radius: 16px;
    background: linear-gradient(90deg, #0078a8, #00a9e0);
    color: white;
    border: none;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
}

@media (max-width: 900px) {
    .weather-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 36px;
    }

    .weather-temp {
        font-size: 58px;
    }
}
</style>
""", unsafe_allow_html=True)


def is_weather_query(message):
    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "hot",
        "cold",
        "rain",
        "wind"
    ]

    message = message.lower()

    for keyword in weather_keywords:
        if keyword in message:
            return True

    return False


def extract_location(message):
    clean_message = message.lower().replace("?", "").replace(".", "")
    words = clean_message.split()

    trigger_words = ["in", "for", "at"]

    for trigger in trigger_words:
        if trigger in words:
            index = words.index(trigger)
            location_words = words[index + 1:]

            if location_words:
                return " ".join(location_words)

    return None


def safe_value(value, unit=""):
    if value is None:
        return "N/A"

    return f"{value}{unit}"


def render_weather_dashboard(weather):
    if not weather["success"]:
        st.error(weather["error"])
        return

    location = html.escape(str(weather["location"]))
    country = html.escape(str(weather["country"]))
    condition = html.escape(str(weather["condition"]))

    temperature = safe_value(weather["temperature"], "°C")
    feels_like = safe_value(weather["feels_like"], "°C")
    humidity = safe_value(weather["humidity"], "%")
    cloud_cover = safe_value(weather["cloud_cover"], "%")
    rain = safe_value(weather["rain"], " mm")
    precipitation = safe_value(weather["precipitation"], " mm")
    wind_speed = safe_value(weather["wind_speed"], " km/h")
    wind_gusts = safe_value(weather["wind_gusts"], " km/h")
    wind_direction = html.escape(
        f"{weather['wind_direction_degrees']}° {weather['wind_direction_text']}"
    )
    day_status = html.escape(str(weather["is_day"]))

    weather_html = f"""
<div class="weather-main-card">
<div class="weather-location">{location}, {country}</div>
<div class="weather-condition">{condition} • {day_status}</div>
<div class="weather-temp">{temperature}</div>
<div class="weather-feels">Feels like {feels_like}</div>
</div>

<div class="weather-grid">
<div class="weather-tile">
<div class="tile-label">Wind</div>
<div class="tile-value">{wind_speed}</div>
<div class="tile-note">Gusts: {wind_gusts}<br>Direction: {wind_direction}</div>
</div>

<div class="weather-tile">
<div class="tile-label">Humidity</div>
<div class="tile-value">{humidity}</div>
<div class="tile-note">Current relative humidity at this location.</div>
</div>

<div class="weather-tile">
<div class="tile-label">Rain</div>
<div class="tile-value">{rain}</div>
<div class="tile-note">Precipitation: {precipitation}</div>
</div>

<div class="weather-tile">
<div class="tile-label">Cloud Cover</div>
<div class="tile-value">{cloud_cover}</div>
<div class="tile-note">Current sky coverage from the weather service.</div>
</div>
</div>
"""

    st.markdown(weather_html, unsafe_allow_html=True)


with st.sidebar:
    st.title(APP_NAME)
    st.write("AI agent prototype with chat and live weather tools.")
    st.markdown("---")

    st.subheader("Capabilities")
    st.write("• AI-powered chat")
    st.write("• Live weather dashboard")
    st.write("• Automatic weather request detection")
    st.write("• Error handling for unknown locations")


st.markdown(f"""
<div class="hero">
<div class="hero-title">{APP_NAME}</div>
<div class="hero-subtitle">An AI agent prototype with intelligent chat and live weather information</div>
</div>
""", unsafe_allow_html=True)


chat_column, weather_column = st.columns([1.55, 1])


with chat_column:
    st.markdown("""
<div class="panel-card">
<h3>AI Chat</h3>
<p>Ask a general question or request live weather for a city.</p>
</div>
""", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input(f"Ask {APP_NAME} something...")

    if user_message:
        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )

        with st.chat_message("user"):
            st.write(user_message)

        if is_weather_query(user_message):
            location = extract_location(user_message)

            if location:
                response = get_weather(location)
            else:
                response = "Please include a city. Example: What is the weather in London?"
        else:
            response = ask_gemini(user_message)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.write(response)


with weather_column:
    st.markdown("""
<div class="panel-card">
<h3>Weather Dashboard</h3>
<p>Enter any city to see live weather information.</p>
</div>
""", unsafe_allow_html=True)

    city = st.text_input(
        "City",
        placeholder="Enter a city",
        value=""
    )

    if st.button("Get Weather"):
        if city.strip():
            weather_data = get_weather_data(city.strip())
            render_weather_dashboard(weather_data)
        else:
            st.warning("Please enter a city name.")