"""
TODO: write documents
"""
from pprint import pprint
from datetime import datetime

import tqdm

import main_lstm
from core.tools.param_set_generator import gen_hparam_set

CPIAUCSUL_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/CPIAUCSL.csv"
SUNSPOT_DATA_E = "/home/ec2-user/environment/AnnEconForecast/data/sunspots.csv"
SUNSPOT_DATA = "/Users/tianyudu/Documents/Academics/EconForecasting/AnnEconForecast/data/sunspots.csv"

SRC_PROFILE = {
    "TRAIN_SIZE": 231,  # Include both training and validation sets.
    "TEST_SIZE": 58,
    "LAGS": [6, 9],
    "VAL_RATIO": 0.2,  # Validation ratio.
    "LEARNING_RATE": [0.01, 0.03],
    "NEURONS": [(32, 64), (64, 128)],
    "EPOCHS": 100,
    "LOG_NAME": "untitled",
    "TASK_NAME": "LastOut LSTM on sunspot",
    "DATA_DIR": SUNSPOT_DATA
}

if __name__ == "__main__":
    profile_set = gen_hparam_set(SRC_PROFILE)
    print("====Sample Configuration====")
    pprint(profile_set[0])
    print("============================")
    start = datetime.now()
    for i in tqdm.trange(len(profile_set), desc="Hyper-Param Profile"):
        PROFILE = profile_set[i]
        main_lstm.core(**PROFILE, profile_record=PROFILE, verbose=False)
    print(f"Total time taken: {datetime.now() - start}")