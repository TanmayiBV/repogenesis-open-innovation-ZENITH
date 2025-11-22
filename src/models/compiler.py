from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import CategoricalAccuracy, TopKCategoricalAccuracy
from config.constants import LEARNING_RATE

def compile_model(model, learning_rate=LEARNING_RATE):
    '''Compile model with optimizer and metrics'''
    optimizer = Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss=CategoricalCrossentropy(label_smoothing=0.1),
        metrics=[
            CategoricalAccuracy(name='accuracy'),
            TopKCategoricalAccuracy(k=3, name='top3_accuracy')
        ]
    )
    
    print(f'✅ Model compiled with learning rate: {learning_rate}')
    return model
