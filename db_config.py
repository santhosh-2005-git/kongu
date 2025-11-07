import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ruthu2006@",  # Replace with your password
        database="farmer_db"
    )
