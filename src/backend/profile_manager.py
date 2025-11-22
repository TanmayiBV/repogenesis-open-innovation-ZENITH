import json
from pathlib import Path

PROFILE_FILE = Path('data/farmer_profile.json')

def save_profile(profile_data):
    '''Save farmer profile to JSON'''
    try:
        PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_FILE, 'w') as f:
            json.dump(profile_data, f, indent=2)
        return {'status': 'success', 'message': '✅ Profile saved successfully'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error saving profile: {str(e)}'}

def load_profile():
    '''Load farmer profile from JSON'''
    try:
        if PROFILE_FILE.exists():
            with open(PROFILE_FILE, 'r') as f:
                return json.load(f)
        else:
            # Return default profile
            return {
                'name': 'Guest Farmer',
                'district': 'Mandya',
                'village': 'Unknown',
                'land_acres': 5.0,
                'crops': ['Rice'],
                'phone': ''
            }
    except Exception as e:
        print(f'Error loading profile: {e}')
        return {'name': 'Guest Farmer', 'district': 'Mandya'}

def update_profile(field, value):
    '''Update specific profile field'''
    profile = load_profile()
    profile[field] = value
    return save_profile(profile)

def get_profile_summary():
    '''Get formatted profile summary'''
    profile = load_profile()
    return f\"\"\"
    👤 **Farmer Profile**
    
    Name: {profile.get('name', 'N/A')}
    Location: {profile.get('village', 'N/A')}, {profile.get('district', 'N/A')}
    Land: {profile.get('land_acres', 0)} acres
    Crops: {', '.join(profile.get('crops', []))}
    \"\"\"

if __name__ == '__main__':
    # Test profile management
    test_profile = {
        'name': 'Test Farmer',
        'district': 'Mandya',
        'village': 'Test Village',
        'land_acres': 10.0,
        'crops': ['Rice', 'Sugarcane']
    }
    result = save_profile(test_profile)
    print(result)
    
    loaded = load_profile()
    print(loaded)
