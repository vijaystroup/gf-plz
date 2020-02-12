""" The data_builder module contains the class DataBuilder which is used to
save all our raw data to a multi-dimensional list we can load to train the
neural network.
"""

import os
import numpy as np
from PIL import Image
from tqdm import tqdm


class DataBuilder:
    """ The DataBuilder class is responsible for going through the data files
    and then saving a list as numpy file with the image and its vector
    classifier. In addition, a count is supplied to see how much data we have.
    """

    def __init__(self):
        """ The __init__ function contains variables we will use for saving our
        data. The LABELS variable indicates when using np.eye(2), vector <1, 0>
        will equate to data/hot whereas vector <0, 1> will equate to data/not_hot.
        """

        self.path = os.path.dirname(__file__)
        self.HOT = f'{self.path}/../data/hot'
        self.NOT_HOT = f'{self.path}/../data/not_hot'
        self.LABELS = {self.HOT: 0, self.NOT_HOT: 1}
        self.data = []
        self.hot_count = 0
        self.not_hot_count = 0
    
    def generator(self):
        """ The generator method opens data, and saves it to a list with their
        proper vector. Then, we shuffle our data so we increase randomness from
        the ai. Finally, we save the list as a numpy file and print our metrics.
        """

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
        np.save(f'{self.path}/data.npy', self.data)
        print(f'Hotties: {self.hot_count}\tNot Hotties: {self.not_hot_count}\n'
              f'Total: {self.hot_count + self.not_hot_count}')


if __name__ == '__main__':
    builder = DataBuilder()
    builder.generator()
