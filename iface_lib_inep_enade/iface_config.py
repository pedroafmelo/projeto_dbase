# -*- coding: UTF-8 -*- 
"""Import modules"""

from os import environ
from os.path import join, dirname, abspath
from dotenv import load_dotenv
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
    host: str
    user: str
    password: str
    db_url: str

class Config:
    """Configuration interface"""

    def __init__(self) -> None:
        """Load instance variables"""
        data = {}
        with open(join(dirname(__file__), "env.yaml"), encoding="utf-8") as file:
            data = load(file, Loader=SafeLoader)

        load_dotenv()

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
        
        self.engine = self.connect_database()
        self.connection = sessionmaker(bind = self.engine)()


        self.uf_codigos = {
            "AC": 12, "AL": 27, "AM": 13, "AP": 16,  
            "BA": 29, "CE": 23, "DF": 53, "ES": 32, 
            "GO": 52, "MA": 21, "MG": 31, "MS": 50, 
            "MT": 51, "PA": 15, "PB": 25, "PE": 26,  
            "PI": 22, "PR": 41, "RJ": 33, "RN": 24,  
            "RO": 11, "RR": 14, "RS": 43, "SC": 42,  
            "SE": 28, "SP": 35, "TO": 17   
        }

        self.columns = {
            "codigo_da_ies": "id_ies",
            "nome_da_ies": "nome_ies",
            "sigla_da_ies": "sigla_ies",
            "categoria_administrativa": "cat_adm",
            "organizacao_academica": "org_acad",
            "codigo_da_area": "id_area",
            "area_de_avaliacao": "area_avaliacao",
            "sigla_da_uf": "sigla_uf",
            "codigo_do_municipio": "id_mun",
            "municipio_do_curso": "mun",
            "codigo_do_curso": "id_curso",
            "modalidade_de_ensino": "modalidade_ensino",
            "no_de_concluintes_inscritos": "num_inscritos",
            "no_de_concluintes_participantes": "num_participantes",
            "conceito_enade_continuo": "enade_continuo",
        }

        self.types = {
            "ano": int, "id_area": int, "id_ies": int, 
            "id_curso": int, "id_mun": int, 
            "num_inscritos": int, "num_participantes": int,
            "enade_continuo": float, "conceito_enade_faixa": int
        }

        self.id_types = {
            "id_area": str, "id_ies": str, 
            "id_local": str, "id_curso": str,
            "id_mun": str, 
        }

    def connect_database(self):
        """Get database 
        connection"""

        engine = create_engine(self.vars.db_url)
        connection = engine.connect()

        try:
            connection.execute(
                text(f"""CREATE DATABASE {self.vars.table}""")
                )
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
