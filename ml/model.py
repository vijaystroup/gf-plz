import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

        self.conv1 = nn.Conv2d(1, 64, 10)
        self.conv2 = nn.Conv2d(64, 128, 10)
        self.conv3 = nn.Conv2d(128, 256, 10)

        x = F.max_pool2d(F.relu(self.conv1(x)), (5, 5))
        x = F.max_pool2d(F.relu(self.conv2(x)), (5, 5))
        x = F.max_pool2d(F.relu(self.conv3(x)), (5, 5))

        self.fc1 = nn.Linear(torch.flatten(x), 512)
        self.fc2 = nn.Linear(512, 2)

    def forward(self, x):
        x = x.view(-1, torch.flatten(x))
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)
