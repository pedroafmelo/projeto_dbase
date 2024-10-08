# -*- Coding: UTF-8 -*- 
"""Import modules"""

from os import path
from shutil import rmtree
from glob import glob
from pandas import read_excel, concat, NA, set_option
from re import sub
from unidecode import unidecode
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Transform:
    """ Iface Transform """

    def __init__(self):
        """ Initialize instance """

        # import local modules
        from iface_lib_inep_enade.iface_config import Config
        from iface_lib_inep_enade.iface_db_model import Model

        self.model = Model
        self.config = Config()

        set_option('future.no_silent_downcasting', True)
        
        self.engine = self.config.engine
        self.data_dir = path.join(self.config.vars.data_dir,
                                  self.config.vars.file_dir)
        
        self.tables_dic = {

            self.model.IES: ["id_ies","nome_ies", 
                        "sigla_ies", "cat_adm", 
                        "org_acad"],

            self.model.Area: ["id_area", "area_avaliacao"],

            self.model.LocalCurso: ["id_local", "id_uf", 
                                "sigla_uf", "id_mun", 
                                "mun"],

            self.model.Curso: ["id_curso", "id_ies",
                           "id_area", "id_local", "modalidade_ensino"],

            self.model.ConceitoEnade: ["ano", "id_curso",
                                   "num_inscritos", "num_participantes",
                                    "enade_continuo", "enade_faixa"]
        }

    def __repr__(self) -> str:
        """ Basic instance 
        representation"""

        return f"Transform and insert data into {str(self.config.vars.table)}"
    
    def __str__(self) -> str:
        """ String instance
        representation"""

        return f"Transform and insert data into {str(self.config.vars.table)}"
    

    def __get_files(self) -> list:
        """ Get files
        return list"""

        try:
            list_files = sorted(glob(f"{self.data_dir}/*/*.xlsx"))

            if len(list_files) == 0:
                print("No new files to process\n")

            return list_files

        except Exception as error:
            raise OSError(error) from error
        
        
    def __transform(self, files_list: list) -> list:
        """ Process datasets 
        return DFs list"""

        processed_files = []

        for file in files_list:
            print(f"Processing file{file}\n")
            try:
                
                data = read_excel(path.join(file))
                
                data.columns = [sub(r"[^a-zA-Z_]", "", 
                                (
                                    unidecode(column.lower().
                                            replace(" ", "_").
                                            replace("__", "_").
                                            replace("*_", ""))
                                            )) 
                                for column in data.columns]
                
                data = (
                    data
                    .rename(columns=self.config.columns)
                    .dropna(subset=["ano", 
                                    "enade_continuo", 
                                    "conceito_enade_faixa"])
                    .assign(
                        enade_faixa = (
                            data["conceito_enade_faixa"]
                            .replace({"SC": 0}).infer_objects()))
                    .astype(self.config.types)
                    .assign(
                        id_uf = (lambda x: x["sigla_uf"]
                                 .map(self.config.uf_codigos).astype(int)),

                        id_local = (lambda x: x["id_uf"]
                                    .astype(str) + x["id_mun"].astype(str))
                    )
                    .replace({NA: None})
                    .astype(self.config.id_types)
                )
                processed_files.append(data)

            except Exception as error:
                raise OSError(error) from error
            
        return processed_files
    

    def __insert(self, files_list: list, table: DeclarativeMeta) -> None:
        """ Insert data
        into database"""

        data_list = []
        
        print(f"Bulk insert into {table().__str__()}")
        try:
            for file in files_list:
                    
                    data = file[self.tables_dic[table]]
                    data_list.append(data)
                
            data = (
                concat(data_list)
                .drop_duplicates(subset=self.tables_dic[table][0])
                .sort_values(self.tables_dic[table][0])
                .dropna(subset=self.tables_dic[table][0])
            )

            if len(data) > 0:
                session = self.config.connection

                for row in data.to_dict("records"):
                    try:
                        query = insert(table).values(row)
                        session.execute(query)
                        session.commit()
                    except IntegrityError:
                        print("Value already exists")
                        session.rollback()
                session.close()
                print("Closed connection\n")
                    
        except Exception as error:
            raise OSError(error) from error
                
        return f"Inserted {table} Data Into Database"


    def __insert_enade(self, files_list: list, table: DeclarativeMeta) -> None:
        """ Insert ConceitoEnade data
        into database"""

        data_list = []

        print(f"Bulk insert into ConceitoEnade")
        try:
            for file in files_list:
                    
                    data = file[self.tables_dic[table]]
                    data_list.append(data)

            data = (concat(data_list))
                
            if len(data) > 0:
                session = self.config.connection

                for row in data.to_dict("records"):
                    try:
                        query = insert(table).values(row)
                        session.execute(query)
                        session.commit()
                    except IntegrityError:
                        print("Value already exists")
                        session.rollback()
                session.close()
                print("Closed connection\n")

            rmtree(self.config.vars.data_dir)
            
        except Exception as error:
            raise OSError(error) from error
        
        return "Inserted Enade Data Into Database"
            

    def __execute(self) -> None:
        """ Populate tables """

        files_list = self.__get_files()

        processed_files_list = self.__transform(files_list)
        self.__insert(processed_files_list, self.model.IES)
        self.__insert(processed_files_list, self.model.Area)
        self.__insert(processed_files_list, self.model.LocalCurso)
        self.__insert(processed_files_list, self.model.Curso)
        self.__insert_enade(processed_files_list, self.model.ConceitoEnade)

        print("All tables populated")
