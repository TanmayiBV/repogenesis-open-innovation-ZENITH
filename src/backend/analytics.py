from datetime import datetime
import json
from pathlib import Path

ANALYTICS_FILE = Path('data/analytics.json')

def track_event(event_type, event_data):
    '''Track user events for analytics'''
    try:
        # Load existing analytics
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE, 'r') as f:
                analytics = json.load(f)
        else:
            analytics = {'events': []}
        
        # Add new event
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': event_data
        }
        analytics['events'].append(event)
        
        # Save analytics
        ANALYTICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        return True
    except Exception as e:
        print(f'Analytics error: {e}')
        return False

def get_usage_stats():
    '''Get usage statistics'''
    try:
        if not ANALYTICS_FILE.exists():
            return {'total_events': 0}
        
        with open(ANALYTICS_FILE, 'r') as f:
            analytics = json.load(f)
        
        events = analytics.get('events', [])
        
        return {
            'total_events': len(events),
            'disease_scans': len([e for e in events if e['type'] == 'disease_scan']),
            'crop_recommendations': len([e for e in events if e['type'] == 'crop_recommendation']),
            'market_checks': len([e for e in events if e['type'] == 'market_check'])
        }
    except:
        return {'total_events': 0}
