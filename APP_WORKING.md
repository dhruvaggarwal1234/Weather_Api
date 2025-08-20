import requests
from flask import Flask, request, render_template

# Replace with your OpenWeatherMap API key
API_KEY = "d9a4d8c7be1e6a4f04a5b0f8a4bc852e"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_weather', methods=['POST'])
def predict_weather():
    if request.method == 'POST':
        location = request.form.get('location')
        try:
            response = fetch_weather_data(location)
            weather_data = parse_weather_data(response)
            return render_template('home.html', **weather_data)
        except Exception:
            return render_template('home.html', error='Please enter a correct place name...')

def fetch_weather_data(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'  # Celsius; use 'imperial' for Fahrenheit
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def parse_weather_data(data):
    main = data['main']
    wind = data['wind']
    sys = data.get('sys', {})
    weather = data['weather'][0]

    return {
        'name': data['name'],
        'country': sys.get('country', ''),
        'temperature_c': main['temp'],
        'temperature_f': round(main['temp'] * 9/5 + 32, 2),
        'weather_condition': weather['description'].title(),
        'wind_speed': wind['speed'],
        'wind_direction': wind.get('deg', 'N/A'),
        'pressure': main['pressure'],
        'humidity': main['humidity'],
    }

if __name__ == '__main__':
    app.run(debug=True)
