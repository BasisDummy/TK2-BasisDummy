import psycopg2
import os

def get_db_connection():
    try:
        # Get database credentials from environment variables

        # Establish a connection to the database
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres.wcqsrpvjyytcuijnlvkm',
            password='eVyy*v7k.dPd$.f',
            host= 'aws-0-ap-southeast-1.pooler.supabase.com',
            port='6543',
           
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute SQL commands to set the search path and list tables in the schema
        cursor.execute("SET SEARCH_PATH TO sijarta")

        return connection

    except psycopg2.Error as e:
        print("Error:", e)


