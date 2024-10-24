# -*- Coding: UTF-8 -*-
"""Authors: Pedro Melo and Gabriel Batista"""

"""Import local modules"""

from iface_lib_inep_enade.iface_extract import Extract
from iface_lib_inep_enade.iface_db_model import Model
from iface_lib_inep_enade.iface_transform import Transform


def main():
    """Handles our
    first SQL Project"""

    Model()._Model__create_tables()
    Extract()._Extract__download()
    Transform()._Transform__execute()
    


if __name__ == "__main__":
    main()
