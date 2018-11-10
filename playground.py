import numpy as np
import pandas as pd
from constants import *
from core.tools.time_series import *
from core.tools.data_import import *
import matplotlib
import matplotlib.pyplot as plt


df = load_dataset(UNRATE_DIR["MAC"])
df_dd = differencing(df, periods=1, order=1)
df_d1 = differencing(df, periods=1, order=2)

lags = [i for i in range(1, 5)]
X, y = gen_supervised(df, predictors=lags)
X, y = clean_nan(X, y)

y = df.copy()
y.columns = ["Targets"]
X = y.shift(1)
X.columns = ["Predictors"]

src = pd.concat([X, y], axis=1)
src.dropna(inplace=True)

lags = 5

samples = list()
for t in range(len(src) - lags - 1):
        obs = src[t:t+lags].values
        samples.append(obs)

s = np.array(samples)

s = gen_supervised_rnn(df, 10)
