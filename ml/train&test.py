from model import Model
import os
from time import strftime
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch
import torch.optim as optim
import torch.nn as nn

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
data = np.load(f'{os.path.dirname(__file__)}/data.npy', allow_pickle=True)
model = Model().double().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()
BATCH_SIZE = 100
EPOCHS = 10
HEIGHT = 80
WIDTH = 64


def load_data():
    X = []
    y = []
    for i in tqdm(data):
        if i[0].shape == torch.Size([HEIGHT, WIDTH]): # some currupt files in dataset
            t = torch.Tensor(i[0]).double()
            t2 = torch.Tensor(i[1])
            X.append(t)
            y.append(t2)

    X = torch.stack(X).view(-1, HEIGHT, WIDTH) # make a tensor of tensors
    X = X / 255.0 # scale pixel values to [0, 1]
    y = torch.stack(y)

    return X, y


def train(train_X, train_y):
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

    X, y = load_data()

    VAL_SIZE = int(len(X) * 0.1) # validation percentage of the data (10%)
    train_X = X[:-VAL_SIZE]
    train_y = y[:-VAL_SIZE]
    test_X = X[-VAL_SIZE:]
    test_y = y[-VAL_SIZE:]

    train(train_X, train_y)
    test(test_X, test_y)
