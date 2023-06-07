__author__ = 'Owner'

import psycopg2
import psycopg2.extensions
from psycopg2 import connect

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#note that we have to import the Psycopg2 extras library!
import psycopg2.extras

class psql_db_interface:

    def __init__(self, database_name):
        self.database_name = database_name
        self.port = 5432
        self.user = "postgres"
        self.password = "postgres"
        # Connect to an existing database
        self.conn = psycopg2.connect(database=self.database_name, port=self.port, user=self.user, password=self.password)
        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def open_cursor(self):
        #self.cur = self.conn.cursor()
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def execute_query(self, queryStr):
        # Query the database and obtain data as Python objects
        self.cur.execute(queryStr)
        return self.cur.fetchall()

    def execute_query_with_param(self, queryStr, tuple_param):
        # Query the database and obtain data as Python objects
        self.cur.execute(queryStr, tuple_param)
        return self.cur.fetchall()

    def execute_query_nr(self, queryStr):
        # Query the database and not return any result to Python
        self.cur.execute(queryStr)

    def execute_query_nr_with_param(self, queryStr, data):
        # Query the database and not return any result to Python
        self.cur.execute(queryStr, data)

    def commit(self):
        # Make the changes to the database persistent
        self.conn.commit()

    def close_db(self):
        # Close communication with the database
        self.conn.close()

    def close_cursor(self):
        self.cur.close()

'''

python -m pip install flask # ------- minimalista ---------- framework para un servidor en la web
pip install jupyter

pip install psycopg2     # driver para postgresql en cuanto a conexion
pip install psycopg2-binary

pip install flask 
pip install flask_script
pip install flask_migratepip 
pip install flask-jsonify 
pip install flask-sqlalchemy 
pip install flask-restful
pip install -U flask-cors

pip install virtualenv

---------------------------------------------------------------------
pip install virtualenv
------ create
       virtualenv env
----------------------- activate <<<--- ( --- luego les detallo --- )
       pip install Flask
'''
