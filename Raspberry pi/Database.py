import mariadb
import sys

class Database(object):
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="user",
                password="password",
                host="localhost",
                database="tp2Infos"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()
    #Ajouter dans la BD
    def add (self,temp, pourcentageOpeningDoor, control, pourcentageManual):
        print ("DATA !")
        try:
            self.cur.execute("INSERT INTO tp2 (temp, pourcentageOpeningDoor, control, pourcentageManual) VALUES (%s, %s, %s, %s);", (temp, pourcentageOpeningDoor, control, pourcentageManual))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        self.conn.commit()