import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

        self.conv1 = nn.Conv2d(1, 64, 10)
        self.conv2 = nn.Conv2d(64, 128, 10)
        self.conv3 = nn.Conv2d(128, 256, 10)

        x = torch.randn(800, 640).view(-1, 1, 800, 640)

        x = F.max_pool2d(F.relu(self.conv1(x)), (5, 5))
        x = F.max_pool2d(F.relu(self.conv2(x)), (5, 5))
        x = F.max_pool2d(F.relu(self.conv3(x)), (5, 5))

        # 2048 is flattened tensor of [1, 256, 4, 2] from previous output
        # print(x.shape)
        self.fc1 = nn.Linear(1024, 512)
        self.fc2 = nn.Linear(512, 2)

    def forward(self, x):
        x = x.view(-1, 1024)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)
