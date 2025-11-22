# 📚 API DOCUMENTATION

## Backend Services

### Weather Service
\\\python
from src.backend import get_weather_forecast

weather = get_weather_forecast('Mandya')
# Returns: {'temperature': 28, 'humidity': 65, ...}
\\\

### Crop Recommender
\\\python
from src.backend import recommend_crops

recommendations = recommend_crops('Mandya', 'Kharif', top_n=3)
# Returns: List of recommended crops with match scores
\\\

### Market Intelligence
\\\python
from src.backend import get_market_prices

prices = get_market_prices('Rice', 'Mandya APMC')
# Returns: Market price data
\\\

## Usage Examples

See examples/ directory for complete usage examples.
