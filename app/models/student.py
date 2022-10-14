import json
from app.general import util

class Student:
    
    def __init__(self, studentId, studentEmail, studentName, studentPhone, studentDetails):
        self.studentId = studentId
        self.studentEmail = studentEmail
        self.studentName = studentName
        self.studentPhone = studentPhone
        # self.studentPassword = studentPassword
        self.studentDetails = studentDetails
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        studentList = []
        for i in range(0, len(databaseResult)):
            studentId = databaseResult[i][0]
            studentEmail = databaseResult[i][1]
            studentName = databaseResult[i][2]
            # studentPassword  = databaseResult[i][3]
            studentPhone = databaseResult[i][4]
            studentDetails = util.getObjectFromBinaryDecode(databaseResult[i][5])
            studentList.append(Student(studentId, studentEmail, studentName, studentPhone, studentDetails).__dict__)
        
        return studentList
        