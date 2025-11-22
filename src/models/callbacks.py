from tensorflow.keras.callbacks import (
    ModelCheckpoint, 
    EarlyStopping, 
    ReduceLROnPlateau,
    TensorBoard
)
from config.constants import MODEL_SAVE_PATH
import datetime

def create_callbacks(model_path=MODEL_SAVE_PATH):
    '''Create training callbacks for model optimization'''
    
    # Model checkpoint
    checkpoint = ModelCheckpoint(
        model_path,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    # Early stopping
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    # Learning rate reduction
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
    
    # TensorBoard
    log_dir = f\"logs/fit/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}\"
    tensorboard = TensorBoard(log_dir=log_dir, histogram_freq=1)
    
    print('✅ Callbacks configured')
    return [checkpoint, early_stop, reduce_lr, tensorboard]
