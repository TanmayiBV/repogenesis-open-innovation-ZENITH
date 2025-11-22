from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from config.constants import IMAGE_SIZE

def create_base_model(input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)):
    '''Create MobileNetV2 base model with ImageNet weights'''
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze all layers initially
    base_model.trainable = False
    
    print(f'✅ Base model loaded: {len(base_model.layers)} layers')
    return base_model

if __name__ == '__main__':
    model = create_base_model()
    model.summary()
