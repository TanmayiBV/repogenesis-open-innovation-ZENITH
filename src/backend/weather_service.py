import requests
from config.api_config import WEATHER_API_KEY, WEATHER_BASE_URL, DISTRICT_COORDS

def get_weather_forecast(district):
    '''Fetch weather data for Karnataka district'''
    try:
        lat, lon = DISTRICT_COORDS.get(district, (12.9716, 77.5946))
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'summary': f\"Current: {data['main']['temp']}°C, {data['weather'][0]['description']}\"
        }
    except Exception as e:
        return {'error': str(e), 'summary': 'Weather data unavailable'}
