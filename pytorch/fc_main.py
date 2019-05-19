"""
Main model for the fully-connected ANN
"""
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import tqdm
import torch
import FcModel
import SlpGenerator

# NOTE: reme mber to uncomment this.
# if __name__ == "__main__":

CPIAUCSUL_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/CPIAUCSL.csv"
SUNSPOT_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/sunspots.csv"

df = pd.read_csv(
    SUNSPOT_DATA,
    index_col=0,
    date_parser=lambda x: datetime.strptime(x, "%Y")
)

df_train, df_test = df[:231], df[-58:]

gen = SlpGenerator.SlpGenerator(df_train)
fea, tar = gen.get_many_to_one(lag=6)
train_dl, val_dl, train_ds, val_ds = gen.get_tensors(
    mode="Nto1", lag=6, shuffle=True, batch_size=32, validation_ratio=0.2
)

net = FcModel.FcNet(num_fea=6, num_tar=1, neurons=(128, 256, 512))
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
criterion = torch.nn.MSELoss()
EPOCHS = 200
class logger:
    def __init__(self):
        self.t, self.v = [], []

    def __repr__(self):
        return f"Log with:\n\ttime={self.t}\n\tvalue={self.v}"

    def add(self, time, value):
        self.t.append(time)
        self.v.append(value)

    def clear(self):
        self.__init__()

    def get_array(self):
        return np.array(self.t), np.array(self.v)

    def get_df(self):
        return pd.DataFrame(data=self.v, index=self.t)

train_log = logger()
val_log = logger()

for i in range(EPOCHS):
    train_loss = 0.
    for batch_idx, (data, target) in enumerate(train_dl):
        # data, target = Variable(data), Variable(target)
        data, target = map(torch.Tensor, (data, target))
        # print(data.shape)
        # print(target.shape)
        # resize data from (batch_size, 1, 28, 28) to (batch_size, 28*28)
        # data = data.view(-1, 6)
        optimizer.zero_grad()
        out = net(data)
        loss = criterion(out, target)
        train_loss += loss.data.item()
        loss.backward()
        optimizer.step()
        # if batch_idx % 50 == 0:
        #     print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        #         i, batch_idx * len(data), len(train_dl.dataset),
        #         100. * batch_idx / len(train_dl), loss.data.item()))
    train_log.add(i, train_loss)
    if i % 10 == 0:
        val_loss = 0.
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(val_dl):
                data, target = map(torch.Tensor, (data, target))
                out = net(data)
                loss = criterion(out, target)
                val_loss += loss.data.item()
        val_log.add(i, val_loss)

    print(f"Epoch: {i}\tTotal Loss: {train_loss:0.6f}\tLatest Val Loss: {val_loss:0.6f}")

# Create plot
plt.plot(train_log.get_df(), label="Train Loss")
plt.plot(val_log.get_df(), label="Validation Loss")
plt.legend()
plt.show()
