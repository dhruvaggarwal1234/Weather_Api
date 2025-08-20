import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

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
            return render_template('home.html', error='Please enter a correct Place name...')

def fetch_weather_data(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def parse_weather_data(data):
    # Extract relevant data
    return {
        'name': data['name'],
        'country': data['sys']['country'],
        'lat': data['coord']['lat'],
        'lon': data['coord']['lon'],
        'temp_c': data['main']['temp'],
        'temp_f': round((data['main']['temp'] * 9/5) + 32, 2),
        'feelslike_c': data['main']['feels_like'],
        'feelslike_f': round((data['main']['feels_like'] * 9/5) + 32, 2),
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'condition_text': data['weather'][0]['description'].title(),
        'condition_icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }

if __name__ == '__main__':
    app.run(debug=True)
