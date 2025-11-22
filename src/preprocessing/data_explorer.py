import os
from pathlib import Path
from config.constants import DATASET_PATH

def get_dataset_structure():
    '''Explore PlantVillage dataset structure'''
    classes = []
    for class_dir in Path(DATASET_PATH).iterdir():
        if class_dir.is_dir():
            count = len(list(class_dir.glob('*.jpg')))
            classes.append({'class': class_dir.name, 'images': count})
    return classes

def validate_dataset():
    '''Check dataset integrity'''
    if not Path(DATASET_PATH).exists():
        raise FileNotFoundError('PlantVillage dataset not found!')
    print(f'✅ Dataset found: {DATASET_PATH}')
    return True
