# -*- coding: utf-8 -*-

"""
Represents a database connection to a MySQL or a PostrgreSQL server
"""

import os

import MySQLdb
import psycopg2

class DBConnection:
    """Symbolize a connection to the SoGreen DB where results are stored"""

    def __init__(self):
        host = os.getenv('SOGREEN_DB_HOST', 'localhost')
        db = os.getenv('SOGREEN_DB_NAME', 'sogreendb')
        user = os.getenv('SOGREEN_DB_USER', 'sogreen')
        passwd = os.getenv('SOGREEN_DB_PASSWD')

        """Initialize a new connection to the database"""
        if os.getenv('SOGREEN_DB_TYPE', 'mysql') == 'mysql':
            self.__con = MySQLdb.connect(
                host=host,
                port=os.getenv('SOGREEN_DB_PORT', 3306),
                db=db,
                user=user,
                passwd=passwd
            )
        else:
            self.__con = psycopg2.connect(
                host=host,
                port=os.getenv('SOGREEN_DB_PORT', 5432),
                dbname=db,
                user=user,
                passwd=passwd
            )

        self.__cursor = self.__con.cursor()

    def make_request(self, query, parameters=()):
        """Make a request to the SoGreen DB"""
        self.__cursor.execute(query, parameters)

        return self.__cursor.fetchall()
