import os
from time import strftime
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch
import torch.optim as optim
import torch.nn as nn
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
data = np.load(f'{os.path.dirname(__file__)}/data.npy', allow_pickle=True)
model = models.vgg16(pretrained=True).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()
BATCH_SIZE = 50
EPOCHS = 1
HEIGHT = 800
WIDTH = 640


def load_data():
    mean=[0.485, 0.456, 0.406]
    std=[0.229, 0.224, 0.225]

    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])
    }

    path = os.path.dirname(__file__)
    data = {
        'train': datasets.ImageFolder(f'{path}/../data/train', data_transforms['train']),
        'val': datasets.ImageFolder(f'{path}/../data/val', data_transforms['val'])
    }
    dataloader = {
        'train': DataLoader(data['train'], batch_size=BATCH_SIZE, shuffle=True),
        'val': DataLoader(data['val'], batch_size=BATCH_SIZE, shuffle=True)
    }

    return dataloader


def train():
    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
            batch_X = train_X[i:i + BATCH_SIZE].double().view(-1, 1, HEIGHT, WIDTH).to(device)
            batch_y = train_y[i:i + BATCH_SIZE].double().to(device)

            model.zero_grad()
            outputs = model(batch_X.double().view(-1, 1, HEIGHT, WIDTH))
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

        print(f'Epoch: {epoch + 1}\tLoss: {loss}')


def test(test_X, test_y):
    correct = 0
    total = 0
    with torch.no_grad():
        for i in tqdm(range(len(test_X))):
            real_value = torch.argmax(test_y[i]).to(device)
            model_out = model(test_X[i].view(-1, 1, HEIGHT, WIDTH).double().to(device))[0]
            predicted_value = torch.argmax(model_out)
            if predicted_value == real_value:
                correct += 1
            total += 1
    print(f'Accuracy: {round(correct / total, 2)}')


# strftime('%Y_%m_%d-%H_%M_%S')
if __name__ == '__main__':
    print(f'Running on {device}')

    data = load_data()

    # train(data['train'])
    # train(data['val'])
