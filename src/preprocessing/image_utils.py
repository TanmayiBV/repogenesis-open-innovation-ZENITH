import numpy as np
from PIL import Image
from config.constants import IMAGE_SIZE

def load_and_preprocess_image(image_path, target_size=IMAGE_SIZE):
    '''Load and preprocess single image for prediction'''
    img = Image.open(image_path).convert('RGB')
    img = img.resize((target_size, target_size))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def preprocess_batch(image_paths, target_size=IMAGE_SIZE):
    '''Preprocess batch of images'''
    batch = []
    for path in image_paths:
        img = Image.open(path).convert('RGB')
        img = img.resize((target_size, target_size))
        batch.append(np.array(img) / 255.0)
    return np.array(batch)

def denormalize_image(img_array):
    '''Convert normalized image back to 0-255 range'''
    return (img_array * 255).astype(np.uint8)
