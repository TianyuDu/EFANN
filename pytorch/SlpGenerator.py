"""
Converting time series to suprevised learning problems.
"""
import numpy as np
import pandas as pd

import data_proc


class GenericGenerator():
    """
    Baseline supervised learning problem generator,
    refer to the structure of methods in this class to write document.
    """

    def __init__(self, main_df: pd.DataFrame, verbose=True):
        self.df = main_df.copy()
        self.v = verbose
        if self.v:
            data_proc.summarize_dataset(self.df)

    def get_many_to_many(self):
        raise NotImplementedError()

    def get_many_to_one(self):
        raise NotImplementedError()


class SlpGenerator(GenericGenerator):
    def __init__(self, main_df: pd.DataFrame, verbose=True):
        super().__init__(main_df=main_df, verbose=verbose)

    def get_many_to_many(
        self,
        lag: int = 6
    ) -> (pd.DataFrame, pd.DataFrame):
        """
        Generate themany-to-many supervised learning problem.
        For each time step t:
            fea(tures): (t, t+1, ..., t+lag)
            tar(gets): (t+1, t+2, ..., t+lag+1)
        """
        lagged = [self.df.shift(i) for i in range(lag + 1)]
        col_names = [f"lag[{i}]" for i in range(lag + 1)]
        frame = pd.concat(lagged, axis=1)
        frame.columns = col_names
        frame.dropna(inplace=True)
        # In N-to-N models.
        fea = frame.iloc[:, 1:]
        tar = frame.iloc[:, :-1]
        assert fea.shape == tar.shape, \
            f"The shape of features and targets in the N-to-N supervised \
                learning problem should be the same. \
                Shapes received: X@{fea.shape}, Y@{tar.shape}."

        if self.v:
            print(f"X@{fea.shape}, Y@{tar.shape}")

        # Cast the datatype
        return fea.astype(np.float32), tar.astype(np.float32)

    def get_many_to_one(self):
        return super().get_many_to_one()

if __name__ == "__main__":
    df2 = pd.DataFrame(list(range(30)))
    g = SlpGenerator(df2)
    fea, tar = g.get_many_to_many()