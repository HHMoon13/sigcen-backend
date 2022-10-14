import json
from app.general import util

class Question:
    
    def __init__(self, questionId, questionTitle, questionGeneralIdea, questionSpecialIdea, 
                 questionNarrative1, questionRequirement1, questionNarrative2, questionRequirement2):
        questionId = self.questionId
        questionTitle = self.questionTitle
        questionGeneralIdea = self.questionGeneralIdea
        questionSpecialIdea = self.questionSpecialIdea 
        questionNarrative1 = self.questionNarrative1 
        questionRequirement1 = self.questionRequirement1 
        questionNarrative2 = self.questionNarrative2 
        questionRequirement2 = self.questionRequirement2 
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        questionList = []
        for i in range(0, len(databaseResult)):
            questionId = databaseResult[i][0]
            questionTitle = databaseResult[i][1]
            questionGeneralIdea = databaseResult[i][2]  
            questionSpecialIdea = databaseResult[i][3]
            questionNarrative1 = databaseResult[i][4]
            questionRequirement1 = databaseResult[i][5]
            questionNarrative2 = databaseResult[i][6]
            questionRequirement2 = databaseResult[i][7]
            questionList.append(Question(questionId, questionTitle, questionGeneralIdea, questionSpecialIdea, 
                                        questionNarrative1, questionRequirement1, questionNarrative2, questionRequirement2).__dict__)
        
        return questionList
 