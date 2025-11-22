from data.databases.schemes_db import SCHEMES_DATABASE

def get_government_schemes(category=None, crop=None):
    '''Find applicable government schemes'''
    schemes = SCHEMES_DATABASE.copy()
    
    # Filter by category
    if category and category != 'All Categories':
        schemes = [s for s in schemes if s.get('category', '').lower() == category.lower()]
    
    # Filter by crop (if scheme has crop-specific targeting)
    if crop and crop != 'All Crops':
        schemes = [s for s in schemes if crop in s.get('applicable_crops', [crop])]
    
    return schemes

def find_schemes_by_farmer_profile(land_size, crops_grown, district):
    '''Recommend schemes based on farmer profile'''
    all_schemes = SCHEMES_DATABASE.copy()
    recommended = []
    
    for scheme in all_schemes:
        score = 0
        
        # Check land size eligibility
        if land_size <= scheme.get('max_land', 999):
            score += 1
        
        # Check if crops match
        scheme_crops = scheme.get('applicable_crops', [])
        if any(crop in scheme_crops for crop in crops_grown):
            score += 2
        
        # State-specific schemes
        if scheme.get('state') == 'Karnataka':
            score += 1
        
        if score > 0:
            recommended.append({
                **scheme,
                'relevance_score': score
            })
    
    return sorted(recommended, key=lambda x: x['relevance_score'], reverse=True)

def format_scheme_details(scheme):
    '''Format scheme information for display'''
    return f\"\"\"
    📜 **{scheme['name']}**
    
    Category: {scheme.get('category', 'General')}
    Benefits: {scheme.get('benefits', 'N/A')}
    Eligibility: {scheme.get('eligibility', 'All farmers')}
    
    How to Apply: {scheme.get('how_to_apply', 'Contact local agriculture office')}
    \"\"\"

if __name__ == '__main__':
    # Test scheme finder
    schemes = get_government_schemes('Subsidy')
    print(f'Found {len(schemes)} subsidy schemes')
