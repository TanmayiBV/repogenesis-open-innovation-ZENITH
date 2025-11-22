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
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(train_dir, val_dir, image_size, batch_size):
    '''Create augmented data generators'''
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    val_gen = val_datagen.flow_from_directory(
        val_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    return train_gen, val_gen
