import json
from app.general import util

class Syndicate:
    
    def __init__(self, syndicateId, sydicateName, exerciseId):
        self.syndicateId = syndicateId
        self.sydicateName = sydicateName
        self.exerciseId = exerciseId
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        syndicateList = []
        for i in range(0, len(databaseResult)):
            syndicateId = databaseResult[i][0]
            sydicateName = databaseResult[i][1]
            exerciseId = databaseResult[i][2]
            syndicateList.append(Syndicate(syndicateId, sydicateName, exerciseId).__dict__)
        
        return syndicateList
        