import json
from app.general import util

class User:
    
    def __init__(self, userEmail, userPhone, userPassword, userDetails):
        self.userEmail = userEmail
        self.userPhone = userPhone
        self.userPassword = userPassword
        self.userDetails = userDetails
        
    @staticmethod
    def toJsonMapFromDatabase(databaseResult):
        userEmail = databaseResult[i][0]
        userPassword = databaseResult[i][1]
        userPhone = databaseResult[i][2]
        userDetails = util.getObjectFromBinaryDecode(databaseResult[i][3])
        return User(userId, userEmail, userPassword, userPhone, createdTime,
                               deleteStatus, activeStatus, emailVerified,
                               phoneVerified, userType, signInType, userDetails).__dict__
        