#!/usr/bin/python3.8
# -*-coding:utf-8 -*-


ERROR_MESSAGE_DOUBLE_SERIAL_NUMBER = "Ce numéro de série a déjà été utilisé!"
ERROR_MESSAGE_PROGRAM_ERROR = "Programmation impossible (NS"


database_connexion_id = {
    "address" : "172.82.83.255",
    "name" : "tracability_db",
    "login" : "user0345",
    "password" : "EY374HSOIE/!"   
}

def main():
    """Main Loop
    """    
    project_name = Mmi.get_project_from_user()         
    project = ProjectNrf(project_name)
    project.load_project()    
    db_service = DataBaseService(**database_connexion_id)  
    while True:        
        try: 
            serial = Mmi.get_serial_from_user()
            db_service.search_double(serial)                  
            hashfield = calcul_hashfield(serial)
            project.serialize_bootloader(hashfield)
            project.merge_files()
            project.program_target() 
            db_service.write_good_record(serial)
            print(f"\x1b[32;1mProgrammation terminée (NS{serial})\x1b[32;0m") 
        except ProjectNrfError:
            Mmi.show_error_to_user(ERROR_MESSAGE_PROGRAM_ERROR+{serial}+")")
            db_service.write_bad_record(serial)
        except DatabaseServiceError:
            Mmi.show_error_to_user(ERROR_MESSAGE_DOUBLE_SERIAL_NUMBER)   
        except MmiError as err:
            Mmi.show_error_to_user(err)
            
class DatabaseServiceError(Exception):
    """Base of Database Service Error
    """    
    pass
            
class DataBaseService():
    """Class with database services tools 
    """    
    def __init__(self, **kwargs) -> None:
        self._address = kwargs.get("address", "localhost")
        self._name = kwargs.get("name", "default_db")        
        if "login" in kwargs:
            self._login = kwargs["login"]
        else:
            raise DatabaseServiceError("Missing login for connexion")        
        if "password" in kwargs:
            self._password = kwargs["password"]
        else:
            raise DatabaseServiceError("Missing login for connexion")
        
    def open_session(self) -> None:
        print(f"\x1b[33;1m[Ouverture de la base: {self._address} {self._name} {self._login} {self._password}]\x1b[32;0m")
        
    def close_session(self) -> None:
        """[summary]
        """        
        print("\x1b[33;1m[Fermeture de la base de donnée]\x1b[32;0m") 
        
    def search_double(self, serial: str) -> None:   
        """[summary]

        Args:
            serial (str): [description]

        Raises:
            DatabaseServiceError: [description]
        """          
        self.open_session() #TODO A refacto   
        print(f"\x1b[33;1m[Recherche dans la base de donnée du NS {serial}]\x1b[32;0m")
        self.close_session()
        if serial in ["100001", "100002", "100003", "100004"]:
            raise DatabaseServiceError("Double found!")  
    
    def write_good_record(self, serial: str) -> None:
        self.open_session()   
        print(f"\x1b[33;1m[Ecriture dans la base de donnée {serial} = 1]\x1b[32;0m")
        self.close_session()    #FIXME A corrigé 
        
    def write_bad_record(self, serial: str) -> None:
        """[summary]

        Args:
            serial (str): [description]

        Raises:
            DatabaseService: [description]
        """        
        self.open_session()   
        print(f"\x1b[33;1m[Ecriture dans la base de donnée {serial} = 0]\x1b[32;0m")
        self.close_session() 
        raise DatabaseService()
        
class ProjectNrfError(Exception):
    """Base Class of Project NRF Error
    """    
    pass

class ProjectNrf():
    """Class for NRF52 Programming
    """    
    def __init__(self, project_name: str) -> None:
        self.__project_name = project_name
        self.__bootloader_filename = None
        self.__sd_filename = None
        self.__bootstrap_filename = None
        self.__applicative_filename = None
        
    @property
    def bootloader_filename(self) -> str:
        return self.__bootloader_filename
    
    @bootloader_filename.setter
    def bootloader_filename(self, value: str) -> None:
        if not isinstance(value, str): 
            raise TypeError()
        self._check_file(value)
        self.__bootloader_filename = value
        
    @property
    def sd_filename(self) -> str:
        return self.__sd_filename
    
    @sd_filename.setter
    def sd_filename(self, value: str) -> None:
        if not isinstance(value, str): 
            raise TypeError()
        self._check_file(value)
        self.__sd_filename = value
        
    @property
    def bootstrap_filename(self) -> str:
        return self.__bootstrap_filename
    
    @bootstrap_filename.setter
    def bootstrap_filename(self, value: str) -> None:
        if not isinstance(value, str): 
            raise TypeError()
        self._check_file(value)
        self.__bootstrap_filename = value
        
    @property
    def applicative_filename(self) -> str:
        return self.__applicative_filename
    
    @applicative_filename.setter
    def applicative_filename(self, value: str) -> None:
        if not isinstance(value, str): 
            raise TypeError()
        self._check_file(value)
        self.__applicative_filename = value         

    def load_project(self) -> None:
        """Load all project files
        """        
        print("************************************")
        print(f"-- Chargement du projet {self.__project_name} --")
        self.bootloader_filename = "bootloader.hex"
        self.sd_filename = "SD.hex"
        self.bootstrap_filename = "bootstrap.hex"
        self.applicative_filename = "applicatif.hex" 
        print("************************************") 
        
    def serialize_bootloader(self, hash: str) -> None:
        """Serialize bootloader with a hash field

        Args:
            hash (bool): hash field
        """        
        print(f"Encodage {self.bootloader_filename} avec code de Hashage {hash}")
        
    def merge_files(self) -> None:
        """Merge all project files
        """        
        print(f">> launch command : mergehex -m {self.bootloader_filename} {self.sd_filename} merge1")
        print(f">> launch command : mergehex -m {self.bootstrap_filename} {self.applicative_filename} merge2")
        print(">> launch command : mergehex -m merge1 merge2 mergefinal")
        
    def program_target(self) -> None:
        """Launch the process of programming target

        Raises:
            ProjectNrfError: [description]
        """            
        print(">> launch_command : nrfjprog --family NRF52 --program mergefinal --chiperase --verify --log")
        print(">> launch_command : nrfjprog --reset")
        raise ProjectNrfError()
        
    def _check_file(self, filename: str) -> None:
        """Check if file exist

        Args:
            filename (str): file to verify
        """        
        # file exist ?
        print(f">>  {filename}...............done")
        
class MmiError(Exception):
    pass

class Mmi():
    """Tool Class for Mmi through a terminal
    """
    SERIAL_NUMBER_QUESTION = "Merci de saisir le numéro de série: "
    PROJECT_NAME_QUESTION = "Saisissez le nom du projet: "
    ERROR_MESSAGE_INVALID_SERIAL_NUMBER = "La saisie n'est pas une numéro de série valide!"
    SERIAL_NUMBER_MIN_VALUE = 100000
    SERIAL_NUMBER_MAX_VALUE = 999999
    
    @classmethod
    def get_project_from_user(cls) -> str:
        """Ask user about project name

        Returns:
            str: project name
        """
        return cls.ask_user(cls.PROJECT_NAME_QUESTION) 
    
    @classmethod
    def get_serial_from_user(cls) -> str:
        """Ask user about serial number

        Returns:
            str: serial number
        """    
        serial =  cls.ask_user(cls.SERIAL_NUMBER_QUESTION)
        cls.verify_serial(serial)
        return serial
    
    @classmethod
    def verify_serial(cls, serial: str) -> None:
        """Verify type and range of serial

        Args:
            serial (str): serial number to verify

        Raises:
            MmiSerialError: Exception raised for a bad serial number value
        """        
        if not (serial.isdigit() and (cls.SERIAL_NUMBER_MIN_VALUE<=int(serial)<cls.SERIAL_NUMBER_MAX_VALUE)):
            raise MmiError(cls.ERROR_MESSAGE_INVALID_SERIAL_NUMBER)

    @staticmethod
    def ask_user(question: str) -> str:
        return input(f"\x1b[37;1m{question}\x1b[37;0m")

    @staticmethod
    def show_error_to_user(error_message: str) -> None:
        print(f"\x1b[31;1m{error_message}\x1b[37;0m")

def calcul_hashfield(serial):
    print(f"Hashage du numero {serial}")
    return "A2312EF76C065EA7C7D"


if __name__ == "__main__":
    main()