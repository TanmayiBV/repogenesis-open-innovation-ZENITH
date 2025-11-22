from src.backend.profile_manager import load_profile
from src.backend.weather_service import get_weather_forecast
from src.backend.market_intelligence import get_market_prices
from data.databases.soil_npk_db import KARNATAKA_SOIL_NPK

def generate_dashboard_data():
    '''Generate comprehensive dashboard data'''
    profile = load_profile()
    district = profile.get('district', 'Mandya')
    crops = profile.get('crops', ['Rice'])
    
    # Get weather
    weather = get_weather_forecast(district)
    
    # Get soil data
    soil_data = KARNATAKA_SOIL_NPK.get(district, {})
    
    # Get market prices for farmer's crops
    market_data = []
    for crop in crops:
        prices = get_market_prices(crop, district)
        if prices:
            market_data.append(prices[0])
    
    return {
        'profile': profile,
        'weather': weather,
        'soil': soil_data,
        'market': market_data,
        'status': 'success'
    }

def calculate_farming_progress(days_since_planting, crop_duration):
    '''Calculate farming cycle progress percentage'''
    if crop_duration <= 0:
        return 0
    progress = (days_since_planting / crop_duration) * 100
    return min(100, max(0, progress))

def get_next_task(days_since_planting, crop):
    '''Suggest next farming task based on crop cycle'''
    tasks = [
        {'day': 0, 'task': 'Land Preparation & Sowing'},
        {'day': 15, 'task': 'First Weeding'},
        {'day': 30, 'task': 'Fertilizer Application'},
        {'day': 45, 'task': 'Pest Inspection'},
        {'day': 60, 'task': 'Second Fertilizer Dose'},
        {'day': 90, 'task': 'Pre-Harvest Preparation'},
        {'day': 120, 'task': 'Harvesting'}
    ]
    
    for i, task in enumerate(tasks):
        if days_since_planting < task['day']:
            days_remaining = task['day'] - days_since_planting
            return {
                'task': task['task'],
                'days_remaining': days_remaining,
                'urgency': 'high' if days_remaining <= 3 else 'medium'
            }
    
    return {'task': 'Crop Complete', 'days_remaining': 0, 'urgency': 'low'}

if __name__ == '__main__':
    # Test dashboard generation
    dashboard = generate_dashboard_data()
    print(f\"Dashboard for: {dashboard['profile']['name']}\")
    print(f\"Weather: {dashboard['weather']['summary']}\")
