import json
from app.general import util

class Exercise:
    
    def __init__(self, exerciseId, exerciseName, courseId, exerciseDetails):
        self.exerciseId = exerciseId
        self.exerciseName = exerciseName
        self.courseId = courseId
        self.exerciseDetails = exerciseDetails
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        exerciseList = []
        for i in range(0, len(databaseResult)):
            exerciseId = databaseResult[i][0]
            exerciseName = databaseResult[i][1]
            courseId = databaseResult[i][2]
            exerciseDetails = databaseResult[i][3]
            exerciseList.append(Exercise(exerciseId, exerciseName, courseId, exerciseDetails).__dict__)
        
        return exerciseList
        