import json
from app.general import util

class Teacher:
    
    def __init__(self, teacherId, teacherEmail, teacherName, teacherPhone, teacherDetails):
        self.teacherId = teacherId
        self.teacherEmail = teacherEmail
        self.teacherName = teacherName
        self.teacherPhone = teacherPhone
        # self.teacherPassword = teacherPassword
        self.teacherDetails = teacherDetails
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        teacherList = []
        for i in range(0, len(databaseResult)):
            teacherId = databaseResult[i][0]
            teacherEmail = databaseResult[i][1]
            teacherName = databaseResult[i][2]
            # teacherPassword = databaseResult[i][3]
            teacherPhone = databaseResult[i][4]
            teacherDetails = util.getObjectFromBinaryDecode(databaseResult[i][5])
            teacherList.append(Teacher(teacherId, teacherEmail, teacherName, teacherPhone, teacherDetails).__dict__)
        
        return teacherList
               