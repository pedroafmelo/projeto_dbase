# -*- coding: UTF-8 -*-
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

        ano = Column(Integer, primary_key=True)

        id_curso = Column(ForeignKey("curso.id_curso", 
                                     ondelete="CASCADE", onupdate="CASCADE"), 
                                     primary_key=True)
        
        num_inscritos = Column(Integer)
        num_participantes = Column(Integer)
        enade_continuo = Column(Float)
        enade_faixa = Column(Integer)

        # Chave estrangeira herdada
        child_curso = relationship("Curso", back_populates="parent_curso")

    class Curso(Base):
        """ Curso Model
        Class """
        __tablename__ = "curso"

        id_curso = Column(Integer, primary_key=True)

        id_ies = Column(ForeignKey("ies.id_ies", 
                                   ondelete="CASCADE",  onupdate="CASCADE"))
        id_area = Column(ForeignKey("area.id_area",
                                   ondelete="CASCADE", onupdate="CASCADE"))
        id_localizacao = Column(ForeignKey("local_curso.id_local", 
                                   ondelete="CASCADE", onupdate="CASCADE"))
        
        modalidade_ensino = Column(String(70))
        grau_academico = Column(String(50))


        # Chave primária a ser herdada
        parent_curso = relationship("ConceitoEnade", back_populates="child_curso", 
                                    cascade="delete, all")
        
        # Chaves estrangeiras herdadas
        child_ies = relationship("IES", back_populates="parent_ies")
        child_area = relationship("Area", back_populates="parent_area")
        child_local = relationship("LocalCurso", back_populates="parent_local")

    class IES(Base):
        """ IES Model
        Class """
        __tablename__ = "ies"

        id_ies = Column(Integer, primary_key=True)
        nome = Column(String(255))
        sigla = Column(String(10))
        cat_adm = Column(String(60))
        org_acad = Column(String(70))

        parent_ies = relationship("Curso", back_populates="child_ies", 
                                  cascade="delete, all")

    class Area(Base):
        """ Area Model
        Class """
        __tablename__ = "area"

        id_area = Column(Integer, primary_key=True)
        area_avaliacao = Column(String(50))

        parent_area = relationship("Curso", back_populates="child_area", 
                                  cascade="delete, all")

    class LocalCurso(Base):
        """ Localizacao 
        Model Class"""
        __tablename__ = "local_curso"

        id_local = Column(Integer, primary_key=True)
        id_uf = Column(Integer)
        sigla_uf = Column(String(2))
        id_mun = Column(Integer)
        mun = Column(String(70))

        parent_local = relationship("Curso", back_populates="child_local",
                                  cascade="delete, all")


    def create_tables(self):
        """ Creates ORM """

        engine = self.config.connect_database()
        try: 
            Base.metadata.create_all(engine)
        except Exception as error:
            raise OSError(error) from error