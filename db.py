import psycopg2
from config import host, user, password
from vcamera import db

class Database:
    connection = None
    cursor = None
    def ConnectToDb(self):
        try:
            Database.connection = psycopg2.connect( 
                    host = host,
                    database="face_temperature",
                    user = user,
                    password = password)
            Database.cursor = Database.connection.cursor()
            print("Connection successefully established !")
        except Exception as _ex:
            print(_ex)

    def InsertToDB(self, temperature):
        try:
            Database.cursor.execute("insert into temp (temperature) values (%s)", [temperature] )
        except Exception as _ex:
            print(_ex)

    def CommitQuery(self):
        Database.connection.commit()

    def CloseConnection(self):
        print("Closing connection")
        Database.connection.close()
        Database.cursor.close()
        print("Connection has been closed")

    def ShowColumns(self):
        rows = Database.cursor.fetchall()
        for r in rows:
            print (f"id {r[0]} name {r[1]}")