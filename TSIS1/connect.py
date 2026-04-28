import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5433"
    )