"""
Main model for the fully-connected ANN
NNAR, neural network auto-regression.
"""
import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import tqdm
from tensorboardX import SummaryWriter

import FcModel
import LogUtility
import SlpGenerator

plt.style.use("seaborn-dark")


# Settings
CPIAUCSUL_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/CPIAUCSL.csv"
SUNSPOT_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/sunspots.csv"
SUNSPOT_DATA_EC2 = "/home/ec2-user/environment/AnnEconForecast/data/sunspots.csv"

# Let's call hyper-parameters profile.
PROFILE = {
    "TRAIN_SIZE": 0.8,  # Include both training and validation sets.
    "TEST_SIZE": 0.2,
    "LAGS": 6,
    "VAL_RATIO": 0.2,  # Validation ratio.
    "BATCH_SIZE": 32,
    "LEARNING_RATE": 0.05,
    "NEURONS": (64, 128),
    "EPOCHS": 100,
    "NAME": "example"  # Name for tensorboard logs.
}


def core(
    profile_record: dict,
    raw_df: pd.DataFrame,
    verbose: bool,
        # set verbose=False when running hyper-parameter search.
    # To ensure progress bar work correctly
    # ==== Parameter from profile ====
    TRAIN_SIZE: Union[int, float],
    TEST_SIZE: Union[int, float],
    LAGS: int,
    VAL_RATIO: float,
    BATCH_SIZE: int,
    LEARNING_RATE: float,
    NEURONS: Tuple[int],
    EPOCHS: int,
    NAME: str    
    ) -> None:
    if verbose:
        input_name = input("Log name ([Enter] for default name): ")
        assert input_name != ""
        LOG_NAME = input_name
    except AssertionError:
        print(f"Default name: {LOG_NAME} is used.")

    df = raw_df.copy()
    
    df_train, df_test = df[:TRAIN_SIZE], df[-TEST_SIZE:]
    print(f"Train&validation size: {len(df_train)}, test size: {len(df_test)}")

    gen = SlpGenerator.SlpGenerator(df_train, verbose=False)
    fea, tar = gen.get_many_to_one(lag=LAGS)
    train_dl, val_dl, train_ds, val_ds = gen.get_tensors(
        mode="Nto1", lag=LAGS, shuffle=True, batch_size=32, validation_ratio=VAL_RATIO
    )

    net = FcModel.Net(num_fea=LAGS, num_tar=1, neurons=NEURONS)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    criterion = torch.nn.MSELoss()
    # train_log = LogUtility.Logger()
    # val_log = LogUtility.Logger()

    with tqdm.trange(EPOCHS) as prg, SummaryWriter(comment=LOG_NAME) as writer:
        for i in prg:
            train_loss = []
            for batch_idx, (data, target) in enumerate(train_dl):
                data, target = map(torch.Tensor, (data, target))
                optimizer.zero_grad()
                out = net(data)
                loss = criterion(out, target)
                train_loss.append(loss.data.item())
                loss.backward()
                optimizer.step()
            # train_log.add(i, np.mean(train_loss))
            # Write MSE
            writer.add_scalars(
                "loss/mse", {"Train": np.mean(train_loss)}, i)
            # Write RMSE

            def func(x): return np.sqrt(np.mean(x))
            writer.add_scalars(
                "loss/rmse", {"Train": func(train_loss)}, i)
            if i % 5 == 0:
                val_loss = []
                with torch.no_grad():
                    for batch_idx, (data, target) in enumerate(val_dl):
                        data, target = map(torch.Tensor, (data, target))
                        out = net(data)
                        loss = criterion(out, target)
                        val_loss.append(loss.data.item())
                # val_log.add(i, np.mean(val_loss))
                writer.add_scalars(
                    "loss/mse", {"Validation": np.mean(val_loss)}, i)

                writer.add_scalars(
                    "loss/rmse", {"Validation": func(val_loss)}, i)
            prg.set_description(
                f"Epoch [{i+1}/{EPOCHS}]: TrainLoss={np.mean(train_loss): 0.3f}, ValLoss={np.mean(val_loss): 0.3f}")
        writer.add_graph(net, (torch.zeros(LAGS)))
        with open(writer.logdir + "/profile.json", "a") as f:
            encoded = json.dumps(PROFILE)
            f.write(encoded)

    # Create plot
    # plt.close()
    # plt.plot(train_log.get_df(ln=True), label="Train Loss")
    # plt.plot(val_log.get_df(ln=True), label="Validation Loss")
    # plt.legend()
    # plt.grid()
    # plt.show()