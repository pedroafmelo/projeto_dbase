# -*- Coding: UTF-8 -*- 
"""Import modules"""

from os import path
from glob import glob
from pandas import Dataframe, read_excel, concat, merge
import numpy as np


class Transform:
    """ Iface Transform """

    def __init__(self):
        """ Initialize instance """

        # import local modules
        from iface_lib_inep_enade.iface_config import Config


        self.config = Config()
        self.data_dir = self.config.vars.data_dir

    def __repr__(self) -> str:
        """ Basic instance 
        representation"""

        return f"Transform and insert data into {str(self.config.vars.table)}"
    
    def __str__(self) -> str:
        """ String instance
        representation"""

        return f"Transform and insert data into {str(self.config.vars.table)}"
    
    def get_files(self) -> list:
        """ Get files
        return list"""

        try:
            list_files = glob(f"{self.data_dir}/*/*.xlsx")

            if len(list_files) == 0:
                print("")


        except Exception as error:
            raise OSError(error) from error
    
