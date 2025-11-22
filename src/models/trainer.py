from config.constants import EPOCHS

def train_model(model, train_gen, val_gen, callbacks, epochs=EPOCHS):
    '''Train disease detection model'''
    print(f'🚀 Starting training for {epochs} epochs...')
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    print('✅ Training completed!')
    return history
