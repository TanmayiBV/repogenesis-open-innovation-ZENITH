def validate_district(district):
    '''Validate Karnataka district name'''
    from data.databases.soil_npk_db import KARNATAKA_SOIL_NPK
    return district in KARNATAKA_SOIL_NPK

def validate_crop(crop):
    '''Validate crop name'''
    from data.databases.crops_db import CROP_DATABASE
    return crop in CROP_DATABASE

def validate_land_size(acres):
    '''Validate land size'''
    try:
        acres_float = float(acres)
        return 0.1 <= acres_float <= 10000
    except:
        return False

def validate_phone(phone):
    '''Validate Indian phone number'''
    import re
    pattern = r'^[6-9]\d{9}$'
    phone_clean = re.sub(r'\D', '', str(phone))
    return bool(re.match(pattern, phone_clean))

def validate_profile_data(profile):
    '''Validate complete profile data'''
    errors = []
    
    if not profile.get('name'):
        errors.append('Name is required')
    
    if not validate_district(profile.get('district', '')):
        errors.append('Invalid district')
    
    if not validate_land_size(profile.get('land_acres', 0)):
        errors.append('Land size must be between 0.1 and 10,000 acres')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
