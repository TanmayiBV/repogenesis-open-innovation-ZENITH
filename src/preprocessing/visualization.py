import matplotlib.pyplot as plt
import numpy as np
from src.preprocessing.data_explorer import get_dataset_structure

def plot_class_distribution(save_path='data/class_distribution.png'):
    '''Visualize class distribution in dataset'''
    classes = get_dataset_structure()
    
    if not classes:
        print('No data to plot')
        return
    
    names = [c['class'][:20] for c in classes]  # Truncate long names
    counts = [c['images'] for c in classes]
    
    plt.figure(figsize=(15, 8))
    plt.barh(names, counts, color='#10B981')
    plt.xlabel('Number of Images')
    plt.title('PlantVillage Dataset - Class Distribution')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f'✅ Plot saved to {save_path}')

def get_class_weights(classes):
    '''Calculate class weights for imbalanced dataset'''
    counts = np.array([c['images'] for c in classes])
    total = counts.sum()
    weights = total / (len(counts) * counts)
    return dict(enumerate(weights))

if __name__ == '__main__':
    plot_class_distribution()
