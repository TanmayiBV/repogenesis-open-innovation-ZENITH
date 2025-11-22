from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

def create_disease_model(num_classes, image_size):
    '''Build MobileNetV2-based disease detection model'''
    base_model = MobileNetV2(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Custom head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    return model, base_model
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

def load_trained_model(model_path):
    '''Load pre-trained disease detection model'''
    return load_model(model_path)

def preprocess_image(image_path, image_size):
    '''Preprocess image for prediction'''
    img = Image.open(image_path).convert('RGB')
    img = img.resize((image_size, image_size))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def predict_disease(model, image_array, class_names):
    '''Get disease prediction with confidence'''
    predictions = model.predict(image_array)[0]
    top_idx = np.argmax(predictions)
    return {
        'disease': class_names[top_idx],
        'confidence': float(predictions[top_idx]),
        'all_predictions': dict(zip(class_names, predictions))
    }
