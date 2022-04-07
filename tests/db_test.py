import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
query = "INSERT INTO users (name,adress,role) VALUES('test_name','test_role','test_adress')"
query2= "DELETE FROM users"

try:
    connection = sqlite3.connect(PROJECT_ROOT + "/database.db")

    connection.execute(query)
    connection.commit()
    print("Insertion into DB successfull.")

    connection.execute(query2)
    connection.commit()
    print("Deletion from DB successfull.")
    
except:
    print("Insertion Failed")
finally:
    connection.close()