from data.databases.crops_db import CROP_DATABASE
from data.databases.soil_npk_db import KARNATAKA_SOIL_NPK

def calculate_npk_match(soil_npk, crop_npk):
    '''Calculate NPK compatibility score'''
    n_diff = abs(soil_npk['N'] - crop_npk['N']) / crop_npk['N']
    p_diff = abs(soil_npk['P'] - crop_npk['P']) / crop_npk['P']
    k_diff = abs(soil_npk['K'] - crop_npk['K']) / crop_npk['K']
    
    match_score = 100 - ((n_diff + p_diff + k_diff) / 3 * 100)
    return max(0, min(100, match_score))

def recommend_crops(district, season='Kharif', top_n=3):
    '''Recommend crops based on soil NPK'''
    soil_data = KARNATAKA_SOIL_NPK.get(district, {})
    recommendations = []
    
    for crop, details in CROP_DATABASE.items():
        if details['season'] == season or season == 'All':
            match = calculate_npk_match(soil_data, details['optimal_npk'])
            recommendations.append({
                'crop': crop,
                'match_score': match,
                'details': details
            })
    
    return sorted(recommendations, key=lambda x: x['match_score'], reverse=True)[:top_n]
