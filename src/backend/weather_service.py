import requests
from src.backend.cache_manager import cache_with_ttl
from config.api_config import WEATHER_API_KEY, WEATHER_BASE_URL, DISTRICT_COORDS

@cache_with_ttl(ttl_seconds=600)  # Cache for 10 minutes
def get_weather_forecast(district):
    '''Fetch current weather for Karnataka district'''
    try:
        coords = DISTRICT_COORDS.get(district, (12.9716, 77.5946))
        lat, lon = coords
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].title(),
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert to km/h
            'pressure': data['main']['pressure'],
            'icon': data['weather'][0]['icon'],
            'summary': f\"{round(data['main']['temp'], 1)}°C, {data['weather'][0']['description']}\",
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        print(f'Weather API Error: {e}')
        return {
            'error': str(e),
            'summary': 'Weather data unavailable',
            'status': 'error'
        }
    except Exception as e:
        print(f'Unexpected error: {e}')
        return {
            'error': 'Unexpected error occurred',
            'summary': 'Weather data unavailable',
            'status': 'error'
        }

if __name__ == '__main__':
    # Test weather service
    weather = get_weather_forecast('Mandya')
    print(weather)

