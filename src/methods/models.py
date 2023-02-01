import pymysql
from dataclasses import dataclass
from src.methods.validations import Validations

class Database:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute(self, query, values=None):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        connection.close()

    def fetch(self, query, values=None):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, values)
        data = cursor.fetchall()
        connection.close()
        return data

    def fetchOne(self, query, values=None):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, values)
        data = cursor.fetchone()
        connection.close()
        return data

@dataclass
class Models:

    data: dict

    def Register(self):
        
        val = Validations(self.data)

        if val.validateRegister():

            name = self.data['name']
            email = self.data['email']
            password = self.data['password']

            

        return False