import enum
from lib2to3.pgen2 import token
import pymysql
from urllib import response

def conection():
    
    con = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
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



def registerUser(email, username, description, image, password, cp):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Users(email, username, description, image, password, zip_code) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %(email, username, description, image, password, cp)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def loginUser(email, password):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, username, description, image, email, is_staff, is_donator, zip_code FROM Users WHERE email = '%s' AND password = '%s'" %(email, password)
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    if resp:
        
        return {
            "id":resp[0][0],
            "username":resp[0][1],
            "email":resp[0][4],
            "is_staff":resp[0][5],
            "description":resp[0][2],
            "image":resp[0][3],
            "is_donator":resp[0][6],
            "zip_code":resp[0][7]
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
    
    query = "SELECT id, username, description, image, is_donator FROM Users WHERE id = '%s'" %id
    
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
    
    query = "SELECT image FROM Profiles WHERE user_id = '%s'" %id
    
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


def createPost(id, name, postContent, image, profileImage, date):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "INSERT INTO Posts (user_id, username, postContent, image, profileImage, date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %(id, name, postContent, image, profileImage, date)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def getPosts():
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, postContent, image, profileImage, date FROM Posts ORDER BY id DESC LIMIT 50"
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    obj = {f"{x}": {"id":y[0], "user_id":y[1], "name":y[2], "postContent":y[3], "image":y[4], "profileImage":y[5], "date":y[6]} for x, y in enumerate(resp)}
    
    return obj

def getPostsById(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, postContent, image, profileImage, date FROM Posts WHERE user_id = '%s' ORDER BY id DESC LIMIT 50" %id
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    obj = {f"{x}": {"id":y[0], "user_id":y[1], "name":y[2], "postContent":y[3], "image":y[4], "profileImage":y[5], "date":y[6]} for x, y in enumerate(resp)}
    
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
    
    query = "UPDATE Users SET is_donator = true WHERE user_id = '%s'" %id
    
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

def getFollow(id, followedId):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT * FROM Follows WHERE follower_id = '%s' AND followed_id = '%s'" %(id, followedId)
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    return resp

def getPostsFollowing(arr):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, postContent, image, profileImage, date FROM Posts WHERE user_id IN (%s) ORDER BY date DESC LIMIT 50" %arr
    
    print(query)
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    obj = {f"{x}": {"id":y[0], "user_id":y[1], "name":y[2], "postContent":y[3], "image":y[4], "profileImage":y[5], "date":y[6]} for x, y in enumerate(resp)}
    
    return obj

def getFollowsId(id):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT followed_id FROM Follows WHERE follower_id = '%s'" %id
    
    cursor.execute(query)
    
    vals = cursor.fetchall()
    
    return vals

def busqueda(value):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = f"SELECT id, username, image FROM Users WHERE username LIKE '%{value}%'" 
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    results = {f"{x}":{"id":y[0], "user":y[1], "image":y[2]} for x, y in enumerate(resp)}
    
    return results

def getAllUsers():
    
    con = conection()
    
    cursor = con.cursor()
    
    query = f"SELECT id, username, image FROM Users ORDER BY usernameme " 
    
    cursor.execute(query)
    
    resp = cursor.fetchall()
    
    results = {f"{x}":{"id":y[0], "user":y[1], "image":y[2]} for x, y in enumerate(resp)}
    
    return results


def emergency(id, name, message, profileImage, latitude, longitude, date, cp):
    
    con = conection() 
    
    cursor = con.cursor()
    
    query = "INSERT INTO Emergencys (user_id, username, message, image, latitude, longitude, date, zip_code) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(id, name, message, profileImage, latitude, longitude, date, cp)
    
    cursor.execute(query)
    
    con.commit()
    
    return True

def getEmergencys(zip):
    
    con = conection()
    
    cursor = con.cursor()
    
    query = "SELECT id, user_id, username, message, image, date, longitude, latitude FROM Emergencys WHERE zip_code = '%a' ORDER BY date DESC LIMIT 5" %zip
    
    cursor.execute(query)
    
    data = cursor.fetchall()
    
    results = {f"{x}":{"id":y[0], "user_id":y[1], "username":y[2], "message":y[3], "image":y[4], "data":y[5], "longitude":y[6], "latitude":y[7]} for x,y in enumerate(data)}
    
    print(results)
    
    return results