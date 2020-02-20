""" This module was orginally used as my model for this project, however with
the complexity and non-simularities in each picture along with the datum size,
this model was not able to train from scratch, and I instead implemented the
method of transfer learning.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    """ This class is the convolutional neural network that the data will train
    on. As the data passes through the channels, starting with 1, it will end
    with 2 channels, hot or not_hot.
    """

    def __init__(self):
        super(Model, self).__init__()

        self.conv1 = nn.Conv2d(1, 64, 5)
        self.conv2 = nn.Conv2d(64, 128, 5)
        self.conv3 = nn.Conv2d(128, 256, 5)

        self.fc1 = nn.Linear(256*6*4, 512)
        self.fc2 = nn.Linear(512, 2)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))
        # flatten data to pass to fully-connected linear layers
        # print(x.shape) #256*6*4
        x = x.view(-1, 256*6*4)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return F.softmax(x, dim=1)
