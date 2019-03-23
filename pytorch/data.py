"""
Mar. 12 2019
Generate one step batch training from fred dataset.
"""
import numpy as numpy
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt


def gen_sup(df: pd.DataFrame, lag: int = 6):
    lagged = [df.shift(i) for i in range(lag + 1)]
    col_names = [f"lag[{i}]" for i in range(lag + 1)]
    frame = pd.concat(lagged, axis=1)
    frame.columns = col_names
    frame.dropna(inplace=True)
    # In N-to-N models, 
    features = frame.iloc[:, 1:]
    target = frame.iloc[:, :-1]
    assert features.shape == target.shape, "Something went wrong."
    print(f"X@{features.shape}, Y@{target.shape}")
    return features, target

if __name__ == "__main__":
    df = pd.read_csv(
        "./sunspot.csv",
        index_col=0,
        date_parser=lambda x: datetime.strptime(x, "%Y")
    )
    # diff = df.diff()
    # diff.dropna(inplace=True)
    # diff.plot()
    # plt.show()
    X, Y = gen_sup(df, lag=60)

    # plt.plot(X.iloc[10, :].values, label="Features")
    # plt.plot(Y.iloc[10, :].values, label="Target")
    # plt.legend()
    # plt.show()
