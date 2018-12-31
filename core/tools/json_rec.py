"""
Created: Dec. 30 2018
This is a file writter writting model parameter to json file.
"""

import json
import os
import datetime
from typing import Union, Dict


class ParamWriter():
    """
    This is a file writer for neural net configuration
    """
    def __init__(
        self,
        file_dir: Union[str, None] = None
    ) -> None:
        """
        Initialization method.
        """
        if file_dir is not None:
            if not os.path.exists(file_dir):
                print("File directory specified not found. trying to create a new one.")
                os.system(f"touch {file_dir}")

        # Admit argument.
        self.file_dir = file_dir

    def write(
            self,
            param: Dict[str, object],
            file_dir: Union[str, None] = None
    ) -> None:
        # ==== Checking Arugment ====
        assert isinstance(param, dict),\
        "Param argument should be a dictionary."
        
        assert all(
                   isinstance(key, str)
                   for key in param.keys()
        ), "All keys of param argument should be string."

        assert not (self.file_dir is None and file_dir is None),\
                "The default file directory is unspecified, you must specify a directory while calling write."

        # ==== End ====
        if file_dir is None:
            # By default, use the default directory.
            file_dir = self.file_dir
        encoded = json.dumps(param)
        with open(file_dir, "a") as f:
            f.write(encoded)

    def read(
            self,
            file_dir: str
    ) -> Dict[str, object]:
        try:
            with open(file_dir, "r") as f:
                encoded = f.read()
                decoded = json.loads(encoded)
            return decoded
        except FileNotFoundError:
            print("The json file given cannot be found, \
                    None is returned.")
            return None
