import os
from pathlib import Path
from config.constants import DATASET_PATH

def get_dataset_structure():
    '''Explore PlantVillage dataset structure'''
    classes = []
    dataset_path = Path(DATASET_PATH)
    
    if not dataset_path.exists():
        print(f'⚠️ Dataset not found at {DATASET_PATH}')
        return []
    
    for class_dir in dataset_path.iterdir():
        if class_dir.is_dir():
            count = len(list(class_dir.glob('*.jpg')))
            classes.append({
                'class': class_dir.name, 
                'images': count
            })
    
    return sorted(classes, key=lambda x: x['images'], reverse=True)

def validate_dataset():
    '''Check dataset integrity'''
    if not Path(DATASET_PATH).exists():
        raise FileNotFoundError(f'PlantVillage dataset not found at {DATASET_PATH}')
    
    structure = get_dataset_structure()
    print(f'✅ Dataset found: {len(structure)} classes detected')
    return True

if __name__ == '__main__':
    validate_dataset()
    classes = get_dataset_structure()
    for cls in classes[:5]:
        print(f\"{cls['class']}: {cls['images']} images\")
