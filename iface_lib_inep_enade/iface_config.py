# -*- coding: UTF-8 -*- 
"""Import modules"""

from os import environ
from os.path import join, dirname, abspath
from yaml import load
from yaml.loader import SafeLoader
from dataclasses import dataclass
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import DatabaseError



@dataclass
class Variables:
    """ Variables dataclass """
    data_dir: str
    file_dir: str
    data_url: str
    table: str
    extension: str
    
    # credentials
    user: str
    password: str
    host: str
    db_url: str

class Config:
    """Configuration interface"""

    def __init__(self) -> None:
        """Load instance variables"""
        data = {}
        with open(join(dirname(__file__), "env.yaml"), encoding="utf-8") as file:
            data = load(file, Loader=SafeLoader)

        self.vars = Variables(
            data_url=data.get("data_url"),
            extension=data.get("extension"),
            data_dir=data.get("data_dir"),
            file_dir=data.get("file_dir"),
            table=data.get("table"),

            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            db_url=""
        )

        self.vars.db_url= (
                f"mysql+mysqlconnector://{self.vars.user}:{self.vars.password}@{self.vars.host}"
                )

    def connect_database(self):
        """Get database 
        connection"""

        engine = create_engine(self.vars.db_url)
        connection = engine.connect()

        try:
            connection.execute(text(f"""CREATE DATABASE {self.vars.table}"""))
            engine = create_engine(
                f"{self.vars.db_url}/{self.vars.table}"
                )
        
        except DatabaseError:
            engine = create_engine(
                f"{self.vars.db_url}/{self.vars.table}"
                )

        return engine
    

    def __repr__(self):
        """ Basic class
        representation """

        return str(self.vars)

    def __str__(self):
        """ Print representation"""

        return str(self.vars)