# -*- Coding: UTF-8 -*-
"""Import local modules"""

from iface_lib_inep_enade.iface_config import Config
from iface_lib_inep_enade.iface_extract import Extract
from iface_lib_inep_enade.iface_db_model import Model
# from iface_lib_inep_enade.iface_transform import Transform


if __name__ == "__main__":
    Model().create_tables()
