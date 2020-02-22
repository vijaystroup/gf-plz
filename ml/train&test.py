import os
import numpy as np
from time import strftime
from tqdm import tqdm
import torch
import torch.optim as optim
import torch.nn as nn
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = models.vgg16(pretrained=True).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss() # using NLL since our last output is log
BATCH_SIZE = 100
EPOCHS = 2


def load_data():
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

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
        'train': datasets.ImageFolder(f'D:\python\gf-plz\data\\train', data_transforms['train']),
        'val': datasets.ImageFolder(f'D:\python\gf-plz\data\\val', data_transforms['val'])
    }
    dataloaders = {
        'train': DataLoader(data['train'], batch_size=BATCH_SIZE, shuffle=True),
        'val': DataLoader(data['val'], batch_size=BATCH_SIZE, shuffle=True)
    }

    return dataloaders


def train(inputs, classes, dataloader):
    # for epoch in range(EPOCHS):
    #     for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
    #         batch_X = train_X[i:i + BATCH_SIZE].double().view(-1, 1, HEIGHT, WIDTH).to(device)
    #         batch_y = train_y[i:i + BATCH_SIZE].double().to(device)

    #         model.zero_grad()
    #         outputs = model(batch_X.double().view(-1, 1, HEIGHT, WIDTH))
    #         loss = criterion(outputs, batch_y)
    #         loss.backward()
    #         optimizer.step()

    #     print(f'Epoch: {epoch + 1}\tLoss: {loss}')

    model.train()

    # freeze models weights and unfreeze few layers we want
    for layer in model.parameters():
        layer.requires_grad = False


    # custom classifier on 6th sequence
    model.classifier[6] = nn.Sequential(
        nn.Linear(4096, 256), # in features from prevous out of model.classifier
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(256, 2),
        nn.LogSoftmax(dim=1)
    ).to(device)
    # print(model.classifier)

    for epoch in range(EPOCHS):
        for inputs, classes in tqdm(dataloader):
            inputs = inputs.to(device)
            classes = classes.to(device)
            # optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, classes)
            loss.backward()
            optimizer.step()
        print(f'Epoch: {epoch + 1}\tLoss: {loss}')


def test(inputs, classes, dataloader):
    correct = 0
    total = 0
    # with torch.no_grad():
    #     for i in tqdm(range(len(test_X))):
    #         real_value = torch.argmax(test_y[i]).to(device)
    #         model_out = model(test_X[i].view(-1, 1, HEIGHT, WIDTH).double().to(device))[0]
    #         predicted_value = torch.argmax(model_out)
    #         if predicted_value == real_value:
    #             correct += 1
    #         total += 1
    # print(f'Accuracy: {round(correct / total, 2)}')

    model.eval()

    with torch.no_grad():
        for inputs, classes in dataloader:
            inputs = inputs.to(device)
            classes = classes.to(device)
            real_value = torch.argmax(classes)
            outputs = model(inputs)[0]
            predicted_value = torch.argmax(outputs)
            if predicted_value == real_value:
                correct += 1
            total += 1
    print(f'Accuracy: {round(correct / total, 2)}')


if __name__ == '__main__':
    print(f'Running on {device}')

    dataloaders = load_data()
    inputs, classes = next(iter(dataloaders['train']))
    train(inputs, classes, dataloaders['train'])
    inputs, classes = next(iter(dataloaders['val']))
    test(inputs, classes, dataloaders['val'])
