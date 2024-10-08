# -* coding: UTF-8 -*- 
"""Import modules"""

from os import path, makedirs, getcwd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import numpy as np
from re import sub


class Extract:
    """Extract Interface"""

    def __init__(self):
        """Initialize instance"""

        # Import local module
        from iface_lib_inep_enade.iface_config import Config

        self.config = Config()
        self.data_dir = path.join(self.config.vars.data_dir,
                             self.config.vars.file_dir)

    def __repr__(self) -> str:
        """Extract Class 
        representation"""

        return f"Extract Class, staging dir: {str(self.data_dir)}"
        
    def __str__(self) -> str:
        """Extract Class
        string representation"""

        return str(self.data_dir)

    def __get_links(self) -> list:
        """Get datasets links
        return list"""
        
        url = self.config.vars.data_url
        links = []

        try:
            session = requests.get(url)
            if not session.ok:
                raise FileNotFoundError(f"Error on read {url}")

            soup = BeautifulSoup(session.content, "html.parser")

            years_tabs = soup.find_all("div", class_ = "tab")
            years = sorted([sub(r"[^0-9\-]", "", elem.text) for elem in years_tabs], 
                           reverse=True)

            for year in years[:4]:
                response = requests.get(f"{url}/{year}")
                if not response.ok:
                        raise FileNotFoundError(f"Error on read INEP Enade {year}")
                soup = BeautifulSoup(response.content, "html.parser")

                links_all = soup.find_all("a", href=True)
                links_filtered = [link["href"] for link in links_all if "conceito_enade" in 
                                link["href"].lower() and "xlsx" in link["href"]][0]
                links.append(links_filtered)

            return links
        
        except Exception as error:
             raise OSError(error) from error
        
    def __check_files(self) -> DataFrame:
        """Check files
        return Dataframe"""
        
        try:
            data = (
                 DataFrame({"url": self.__get_links()})
                 .assign(
                      filename = lambda x: x["url"].str.split("/").str[-1],
                      year = lambda x: x["filename"].apply(
                           lambda y: sub(r"[^0-9]", "", y)).astype(int),
                      _id = lambda x: self.config.vars.table + "_" + str(x["year"])              
                 )
            )

            if len(data) == 0:
                 raise FileNotFoundError(
                      f"Error on read {self.config.vars.data_url}"
                      )
            return data

        except Exception as error:
            raise OSError(error) from error
    
    def __download(self) -> None:
        """Download datasets"""
         
        links = self.__check_files()

        try: 
            for link in links.to_dict("records"):
                filename = link["filename"]
                year = link["year"]

                makedirs(path.join(self.data_dir, str(year)), 
                         exist_ok=True)
                
                url = link["url"]

                request = requests.get(url)
                if not request.ok:
                    raise FileNotFoundError(f"Error on Download INEP Enade {year}")

                with open(path.join(self.data_dir, str(year),
                                    filename), "wb") as file:
                    
                    file.write(request.content)
                    print(f"Downloaded {filename} file successfully\n")
        
            print("Download files finished\n")
        
        except Exception as error:
            raise OSError("Could not download INEP - ENADE")
