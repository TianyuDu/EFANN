"""
This script contains various types of loss metric report function.
"""

import numpy as np
import pandas as pd
from typing import Dict


def merged_scores(
    actual: pd.DataFrame,
    pred: pd.DataFrame,
    verbose: bool = False
) -> Dict[str, float]:
    acceptable_types = (
        float, int, np.float32, np.float64, np.int32, np.int64)

    def check_type(df): return all(
        type(x) in acceptable_types for x in df.values.reshape(-1))

    def get_types(df): return set([type(x) for x in df.values.reshape(-1)])

    assert check_type(actual),\
        f"Invalid types found in actual series,\nTypes found {get_types(actual)}"
    assert check_type(pred),\
        f"Invalid types found in prediction series,\nTypes found {get_types(pred)}"

    metric_dict = dict()

    act_val = actual.values.reshape(-1,)
    pred_val = pred.values.reshape(-1,)

    def MAE(x, y):
        return np.mean(np.abs(x - y))

    def MSE(x, y):
        return np.mean((x - y)**2)

    def RMSE(x, y):
        return np.sqrt(MSE(x, y))

    def MAPE(x, y):
        return np.mean(np.abs((x - y) / y))

    # mean absolute error
    metric_dict["mae"] = MAE(pred_val, act_val)
    # mean squared error
    metric_dict["mse"] = MSE(pred_val, act_val)
    # root mean squared error
    metric_dict["rmse"] = RMSE(pred_val, act_val)
    # mean absolute percentage error
    metric_dict["mape"] = MAPE(pred_val, act_val)

    if verbose:
        print("Loss Summary:")
        for m, v in metric_dict.items():
            print(f"\t{m}={v}")

    return metric_dict
