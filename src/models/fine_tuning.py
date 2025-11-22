def unfreeze_base_model(model, unfreeze_from=100):
    '''Unfreeze base model layers for fine-tuning'''
    base_model = model.layers[0]
    
    # Unfreeze from specific layer
    for layer in base_model.layers[:unfreeze_from]:
        layer.trainable = False
    
    for layer in base_model.layers[unfreeze_from:]:
        layer.trainable = True
    
    trainable_count = sum([1 for layer in base_model.layers if layer.trainable])
    print(f'✅ Fine-tuning enabled: {trainable_count} layers unfrozen')
    
    return model
