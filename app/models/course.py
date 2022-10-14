import json
from app.general import util

class Course:
    
    def __init__(self, courseId, courseName, madeBy, courseDetails):
        self.courseId = courseId
        self.courseName = courseName
        self.madeBy = madeBy
        self.courseDetails = courseDetails
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        courseList = []
        for i in range(0, len(databaseResult)):
            courseId = databaseResult[i][0]
            courseName = databaseResult[i][1]
            madeBy = databaseResult[i][2]
            courseDetails = databaseResult[i][3]
            courseList.append(Course(courseId, courseName, madeBy, courseDetails).__dict__)
        
        return courseList
        