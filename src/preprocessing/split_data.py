import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

def create_train_val_split(source_dir, output_dir, val_split=0.2, seed=42):
    '''Split dataset into training and validation sets'''
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    train_dir = output_path / 'train'
    val_dir = output_path / 'val'
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    for class_dir in source_path.iterdir():
        if not class_dir.is_dir():
            continue
        
        images = list(class_dir.glob('*.jpg'))
        train_imgs, val_imgs = train_test_split(
            images, 
            test_size=val_split, 
            random_state=seed
        )
        
        # Create class directories
        (train_dir / class_dir.name).mkdir(exist_ok=True)
        (val_dir / class_dir.name).mkdir(exist_ok=True)
        
        print(f'Processing {class_dir.name}: {len(train_imgs)} train, {len(val_imgs)} val')

if __name__ == '__main__':
    print('Use this function to split your dataset if needed')
