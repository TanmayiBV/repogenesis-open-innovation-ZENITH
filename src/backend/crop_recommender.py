from data.databases.crops_db import CROP_DATABASE
from data.databases.soil_npk_db import KARNATAKA_SOIL_NPK

def calculate_npk_match(soil_npk, crop_npk):
    '''Calculate NPK compatibility score (0-100)'''
    try:
        n_diff = abs(soil_npk['N'] - crop_npk['N']) / max(crop_npk['N'], 1)
        p_diff = abs(soil_npk['P'] - crop_npk['P']) / max(crop_npk['P'], 1)
        k_diff = abs(soil_npk['K'] - crop_npk['K']) / max(crop_npk['K'], 1)
        
        avg_diff = (n_diff + p_diff + k_diff) / 3
        match_score = max(0, min(100, 100 - (avg_diff * 100)))
        
        return round(match_score, 2)
    except:
        return 50.0  # Default moderate match

def recommend_crops(district, season='Kharif', top_n=5):
    '''Recommend crops based on soil NPK data'''
    soil_data = KARNATAKA_SOIL_NPK.get(district, {'N': 200, 'P': 50, 'K': 50, 'pH': 6.5})
    recommendations = []
    
    for crop_name, crop_details in CROP_DATABASE.items():
        # Filter by season if specified
        if season != 'All' and crop_details.get('season') != season:
            continue
        
        match_score = calculate_npk_match(soil_data, crop_details['optimal_npk'])
        
        recommendations.append({
            'crop': crop_name,
            'match_score': match_score,
            'yield_per_acre': crop_details.get('yield_per_acre', 0),
            'duration_days': crop_details.get('duration_days', 0),
            'water_requirement': crop_details.get('water_requirement', 'Medium'),
            'market_price': crop_details.get('market_price', 3000),
            'estimated_revenue': crop_details.get('yield_per_acre', 0) * crop_details.get('market_price', 3000)
        })
    
    # Sort by match score
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return recommendations[:top_n]

if __name__ == '__main__':
    # Test recommendation system
    recs = recommend_crops('Mandya', 'Kharif', 3)
    for rec in recs:
        print(f\"{rec['crop']}: {rec['match_score']}% match\")
