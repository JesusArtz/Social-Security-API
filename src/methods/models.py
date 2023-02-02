from dataclasses import dataclass

import pymysql

from src.methods.validations import Validations


class Database:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute(self, query, values=None):
        cursor = self.connectioncursor()

        cursor.execute(query, values)
        self.connectioncommit()
        self.connectionclose()

    def fetch(self, query, values=None):
        cursor = self.connectioncursor()

        cursor.execute(query, values)
        data = cursor.fetchall()

        self.connectionclose()

        return data

    def fetchOne(self, query, values=None):
        cursor = self.connectioncursor()

        cursor.execute(query, values)
        data = cursor.fetchone()

        self.connectionclose()

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
