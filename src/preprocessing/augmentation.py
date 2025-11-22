from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config.constants import IMAGE_SIZE, BATCH_SIZE

def create_train_generator(train_dir, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE):
    '''Create augmented training data generator'''
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest',
        validation_split=0.2
    )
    
    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=(target_size, target_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    return train_gen

def create_validation_generator(train_dir, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE):
    '''Create validation data generator'''
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    val_gen = val_datagen.flow_from_directory(
        train_dir,
        target_size=(target_size, target_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return val_gen
