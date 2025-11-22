import numpy as np
from tensorflow.keras.models import load_model
from src.preprocessing.image_utils import load_and_preprocess_image

def load_trained_model(model_path):
    '''Load pre-trained disease detection model'''
    print(f'Loading model from {model_path}...')
    model = load_model(model_path)
    print('✅ Model loaded successfully')
    return model

def predict_disease(model, image_path, class_names):
    '''Predict disease from image'''
    img_array = load_and_preprocess_image(image_path)
    predictions = model.predict(img_array, verbose=0)[0]
    
    top_idx = np.argmax(predictions)
    confidence = float(predictions[top_idx])
    
    # Get top 3 predictions
    top3_indices = np.argsort(predictions)[-3:][::-1]
    top3_results = [
        {
            'disease': class_names[idx],
            'confidence': float(predictions[idx])
        }
        for idx in top3_indices
    ]
    
    return {
        'disease': class_names[top_idx],
        'confidence': confidence,
        'top3': top3_results,
        'all_predictions': dict(zip(class_names, predictions.tolist()))
    }
