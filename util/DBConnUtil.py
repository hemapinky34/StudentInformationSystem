import mysql.connector
from mysql.connector import Error

class DBConnUtil:
    @staticmethod
    def get_connection(connection_params):
        try:
            connection = mysql.connector.connect(
                host=connection_params['host'],
                database=connection_params['database'],
                user=connection_params['user'],
                password=connection_params['password']
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None