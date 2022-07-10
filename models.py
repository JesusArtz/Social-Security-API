import sqlite3
from urllib import response

def conection():
    
    con = sqlite3.connect('database.db')
    
    return con





def registerUser(email, username, password):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Users(email, username, password) VALUES ('%s', '%s', '%s')" %(email, username, password)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def loginUser(email, password):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, username, email FROM Users WHERE email = '%s' AND password = '%s'" %(email, password)
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    if resp:
        
        return {
            "id":resp[0][0],
            "username":resp[0][1],
            "email":resp[0][2]
        }
        
    return False


def generateSession(id, token):
    
    con = conection()

    cursor = con.cursor()
    
    queryValidate = "SELECT token FROM Sessions WHERE user_id = '%s'" %id
    
    cursor.execute(queryValidate)
    
    respValidation = cursor.fetchone()
    
    if respValidation:
        
        return False
    
    query = "INSERT INTO Sessions (user_id, token) VALUES ('%s', '%s')" %(id, token)

    cursor.execute(query)
    
    con.commit()
    
    return True

def deleteSession(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "DELETE FROM Sessions WHERE user_id = '%s'" %id
    
    cursor.execute(query)
    
    con.commit()

    return True


def getHash(email):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT password FROM Users WHERE email = '%s'" %email
    
    cursor.execute(query)
    
    resp = cursor.fetchone()
    
    return resp


