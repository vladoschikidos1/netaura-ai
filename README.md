# NetAura AI

A Python chat and weather application I built for my Cisco summer project. It uses Gemini to answer general questions and Open-Meteo to get current weather information, with a Streamlit interface.

The aim was to practise connecting an AI model and an external data source in one application. This is a student prototype with simple keyword-based routing.

## Features

- Ask general questions using the Gemini API.
- Ask weather questions such as "What is the weather in London?"
- Search for a city directly in the weather dashboard.
- View temperature, feels-like temperature, humidity, rain, cloud cover, wind speed, gusts and direction.
- See messages for missing locations and common API connection problems.
- View the chat messages from the current Streamlit session.

## Technologies

Python, Streamlit, Google Gen AI SDK, Requests, Open-Meteo Geocoding API and Open-Meteo Weather API.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, keyword routing and weather display |
| `ai_chat.py` | Sends a message to Gemini and returns its response |
| `weather.py` | Looks up city coordinates and retrieves current weather |
| `requirements.txt` | Python packages needed to run the application |
| `.gitignore` | Excludes local credentials, environments and generated files from Git |

## Run locally

You need Python 3, an internet connection and a Gemini API key for the general chat feature. The weather feature works without a Gemini key.

Download or clone the repository, then open a terminal inside the project folder.

### 1. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install the packages

```bash
python -m pip install -r requirements.txt
```

### 3. Set the Gemini API key

The app reads the `GEMINI_API_KEY` environment variable. Set it in the terminal session or PyCharm run configuration used to start the app. Keep the actual value out of the source files and Git commits.

For a macOS terminal, enter the following command, paste your key when the terminal waits for input, and press Return. The key will not be displayed as you type:

```bash
read -r -s GEMINI_API_KEY
export GEMINI_API_KEY
```

If using a PyCharm run configuration, add an environment variable named `GEMINI_API_KEY` with your key as its value.

### 4. Start the application

Run this in the same terminal session:

```bash
python -m streamlit run app.py
```

Open the local address shown by Streamlit. Stop the application with `Ctrl+C`.

## How it works

The interface checks the message for weather keywords. For a weather question, it tries to extract the location after words such as "in", "for" or "at". The weather module converts that location into coordinates and uses them to request current conditions.

Other questions are sent to Gemini. The model is configured in `ai_chat.py` as `gemini-2.5-flash`.

The separate weather dashboard uses the city entered in its search box and calls the same weather module.

## Current limitations

- Weather detection and location extraction use simple rules, so some messages can be misunderstood.
- The weather tool returns current conditions, not a future forecast.
- Messages appear in the current session, but each Gemini request contains only the latest user message. There is no saved conversation history or conversation context sent to the model.
- General chat depends on the API key, model access and the service's usage limits.

## What I learned

This project helped me practise working with API requests and JSON responses, separating code into modules, handling errors and connecting Python functions to a graphical interface.

## Possible improvements

- Improve weather detection and location extraction.
- Add conversation context to the AI chat.
- Add automated tests for routing and weather data processing.
- Improve the distinction between a missing location and a failed geocoding request.
- Add a forecast view alongside current weather.
