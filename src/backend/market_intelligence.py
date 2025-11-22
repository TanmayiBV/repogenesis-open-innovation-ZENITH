import random
from datetime import datetime, timedelta

# Demo Market Data (Karnataka Mandis)
DEMO_MANDI_PRICES = {
    'Mandya APMC': {
        'Rice': 2800, 'Ragi': 3500, 'Maize': 2200, 'Sugarcane': 3100,
        'Cotton': 8500, 'Tomato': 1200, 'Potato': 1800, 'Arecanut': 45000
    },
    'Raichur APMC': {
        'Rice': 2950, 'Ragi': 3600, 'Maize': 2300, 'Sugarcane': 3000,
        'Cotton': 8700, 'Tomato': 1100, 'Potato': 1700, 'Arecanut': 44000
    },
    'Shimoga APMC': {
        'Rice': 2750, 'Ragi': 3400, 'Maize': 2100, 'Sugarcane': 3200,
        'Cotton': 8300, 'Tomato': 1300, 'Potato': 1900, 'Arecanut': 48000
    },
    'Hubli APMC': {
        'Rice': 2850, 'Ragi': 3550, 'Maize': 2250, 'Sugarcane': 3050,
        'Cotton': 8600, 'Tomato': 1400, 'Potato': 1850, 'Arecanut': 46000
    }
}

def get_market_prices(crop, district='All'):
    '''Get market prices for crop across mandis'''
    results = []
    
    if district == 'All':
        mandis = DEMO_MANDI_PRICES.keys()
    else:
        mandis = [district] if district in DEMO_MANDI_PRICES else []
    
    for mandi in mandis:
        price = DEMO_MANDI_PRICES[mandi].get(crop, 3000)
        
        # Add realistic variation
        variation = random.uniform(-0.05, 0.05)
        current_price = int(price * (1 + variation))
        
        results.append({
            'mandi': mandi,
            'crop': crop,
            'price': current_price,
            'unit': 'per quintal',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'trend': random.choice(['up', 'down', 'stable'])
        })
    
    return results

def get_price_comparison(crop, districts):
    '''Compare prices across multiple districts'''
    comparison = []
    
    for district in districts:
        if district in DEMO_MANDI_PRICES:
            price = DEMO_MANDI_PRICES[district].get(crop, 3000)
            comparison.append({
                'district': district,
                'price': price
            })
    
    return sorted(comparison, key=lambda x: x['price'], reverse=True)

if __name__ == '__main__':
    # Test market intelligence
    prices = get_market_prices('Rice', 'All')
    for p in prices:
        print(f\"{p['mandi']}: ₹{p['price']}/{p['unit']}\")
