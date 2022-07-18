import models as md

class Conditionals:
    
    def __init__(self):
        
        self.true = True
        self.false = False
        
    def NullData(self, data):
        
        if data:
            
            return self.true
        
        return error
        
        
    def ExistentEmailOrUsername(self, data):
        
        username = data['username']
        email = data['email']
        
        existentEmail = md.getExistEmail(email)
        existentUsername = md.getExistUsername(username)
        
        if existentEmail or existentUsername:
            
            return self.true
        
        return error
    
    
    