import os
import numpy as np
from PIL import Image
from tqdm import tqdm

class DataBuilder:
    def __init__(self):
        self.HOT = '../data/hot'
        self.NOT_HOT = '../data/not_hot'
        self.LABELS = {self.HOT: 1, self.NOT_HOT: 0}
        self.data = []
        self.hot_count = 0
        self.not_hot_count = 0
    
    def generator(self):
        for label in self.LABELS:
            for f in tqdm(os.listdir(label)):
                try:
                    f_path = os.path.join(label, f)
                    im = Image.open(f_path)
                    self.data.append(
                        [np.array(im), np.eye(2)[self.LABELS[label]]]
                    )

                    if label == self.HOT:
                        self.hot_count += 1
                    else:
                        self.not_hot_count += 1
                except Exception as e:
                    print(f'Error: {e}')
        
        np.random.shuffle(self.data)
        np.save('data.npy', self.data)
        print(f'Hotties: {self.hot_count}\tNot Hotties: {self.not_hot_count}')


if __name__ == '__main__':
    builder = DataBuilder()
    builder.generator()
