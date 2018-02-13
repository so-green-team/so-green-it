# -*- coding: utf-8 -*-

"""
Represents a database connection to a MySQL or a PostrgreSQL server
"""

import MySQLdb.cursors
import MySQLdb
import psycopg2

class DBConnection:
    """Symbolize a connection to the SoGreen DB where results are stored"""

    def __init__(self, db_type, host, port, db, user, passwd):
        """Initialize a new connection to the database"""
        if db_type == 'mysql':
            self.__con = MySQLdb.connect(
                host=host,
                port=port,
                db=db,
                user=user,
                passwd=passwd,
                cursorclass=MySQLdb.cursors.DictCursor
            )
        else:
            self.__con = psycopg2.connect(
                host=host,
                port=port,
                dbname=db,
                user=user,
                passwd=passwd
            )

        self.__cursor = self.__con.cursor()

    def make_request(self, query, parameters=[]):
        """Make a request to the SoGreen DB"""
        self.__cursor.execute(query, parameters)
        self.__con.commit()

        return self.__cursor.fetchall()
