# -*- coding: UFT-8 -*-
"""Import modules"""
from sqlalchemy import ForeignKey, String, Float, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Model:
    """ Class
    Database Model
    """

    def __init__(self):
        """ Initialize instance """
        
        # import local modules
        from iface_lib_inep_enade.iface_config import Config

        self.config = Config()

    class ConceitoEnade(Base):
        """ Conceito Enade
        Model Class """
        __tablename__ = "conceito_enade"

        ano = Column()
        