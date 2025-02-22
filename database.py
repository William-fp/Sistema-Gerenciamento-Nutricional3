from pymongo import MongoClient

class DBConnection:
    def __init__(self):
        self.__connection_string = "mongodb+srv://hunttergx:enT2SXkYr7ezDOUJ@informacaonutricional.dgmeq.mongodb.net/?retryWrites=true&w=majority&appName=InformacaoNutricional"
        self.__database_name = "InformacaoNutricional"
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__[self.database_name]

    def get_db_connection(self):
        return self.__db_connection
    
    def get_db_client(self):
        return self.__client