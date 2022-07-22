from lib2to3.pgen2 import token
import pymysql
from urllib import response

def conection():
    
    con = pymysql.connect(
        host='db-mysql-sfo3-50689-do-user-9517177-0.b.db.ondigitalocean.com',
        user='doadmin',
        password='AVNS_bsBS1_49gRb0WcTJji6',
        port=25060,
        db='defaultdb'
    )
    
    return con


def getExistUsername(username):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT * FROM Users WHERE username = '%s'" %username
    
    cursor.execute(query)
    
    response = cursor.fetchall()
    
    if response:
        
        return False
    
    return True

def getExistEmail(email):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT * FROM Users WHERE email = '%s'" %email
    
    cursor.execute(query)
    
    response = cursor.fetchall()
    
    if response:
        
        return False
    
    return True



def registerUser(email, username, description, image, password):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Users(email, username, description, image, password) VALUES ('%s', '%s', '%s', '%s')" %(email, username, description, image, password)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def loginUser(email, password):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, username, description, image, email, is_active, is_staff FROM Users WHERE email = '%s' AND password = '%s'" %(email, password)
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    if resp:
        
        return {
            "id":resp[0][0],
            "username":resp[0][1],
            "email":resp[0][4],
            "is_active":resp[0][5],
            "is_staff":resp[0][6],
            "description":resp[0][2],
            "image":resp[0][3],
            
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

def deleteSession(token):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "DELETE FROM Sessions WHERE token = '%s'" %token
    
    cursor.execute(query)
    
    con.commit()

    return True


def getHash(email):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT password FROM Users WHERE email = '%s'" %email
    
    cursor.execute(query)
    
    resp = cursor.fetchone()
    
    print(resp)
    
    return resp

def createProfile(id, name, description, imageProfile):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Profiles (user_id, name, description, imageUrl) VALUES ('%s', '%s', '%s', '%s')" %(id, name, description, imageProfile)
    
    queryUpdate = "UPDATE Users SET is_active = true WHERE id = '%s'" %id
    
    cursor.execute(query)
    
    cursor.execute(queryUpdate)
    
    con.commit()
    
    return True

def getProfile(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, username, description, imageUrl FROM Profiles WHERE user_id = '%s'" %id
    
    cursor.execute(query)
    
    data = cursor.fetchone()

    
    if data:
        
        return data
    
    return False

def getIdFromToken(token):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT user_id FROM Sessions WHERE token = '%s'" %token
    
    cursor.execute(query)
    
    result = cursor.fetchone()
    
    return result

def getImageFromId(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT imageUrl FROM Profiles WHERE user_id = '%s'" %id
    
    cursor.execute(query)
    
    image = cursor.fetchone()
    
    return image[0]

def getUserById(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, username, email, is_active, is_staff FROM Users WHERE id = '%s'" %id
    
    cursor.execute(query)
    
    resp = cursor.fetchone()
    
    return resp

def getSessionById(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT token FROM Sessions WHERE user_id = '%s'" %id
    
    cursor.execute(query)
    
    resp = cursor.fetchone()
    
    return resp


def createPost(id, username, name, postContent, image, profileImage):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Posts (user_id, username, name, postContent, image, profileImage) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %(id, username, name, postContent, image, profileImage)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def getPosts():
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, name, postContent, image, profileImage FROM Posts ORDER BY id DESC LIMIT 50"
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    obj = {f"{x}": {"id":y[0], "user_id":y[1], "username":y[2], "name":y[3], "postContent":y[4], "image":y[5], "profileImage":y[6]} for x, y in enumerate(resp)}
    
    return obj

def getPostsById(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, name, postContent, image, profileImage FROM Posts WHERE user_id = '%s' ORDER BY id DESC LIMIT 50" %id
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    obj = {f"{x}": {"id":y[0], "user_id":y[1], "username":y[2], "name":y[3], "postContent":y[4], "image":y[5], "profileImage":y[6]} for x, y in enumerate(resp)}
    
    return obj

def getIdByUsername(username):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id FROM Users WHERE username = '%s'" %username
    
    cursor.execute(query)
    
    data = cursor.fetchone()
    
    return data[0]

def setDonator(username):
    
    con = conection()
    
    cursor = con.cursor()
    
    id = getIdByUsername(username)
    
    query = "UPDATE Profiles SET is_donator = true AND tier_donator = '1' WHERE user_id = '%s'" %id
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def setFollow(follower, followed):

    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Follows (follower_id, followed_id) VALUES ('%s', '%s')" %(follower, followed)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def getFollow(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT * FROM Follows WHERE follower = "