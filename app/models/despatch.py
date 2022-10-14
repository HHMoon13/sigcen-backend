import json
from app.general import util

class Despatch:
    def __init__(self, despatchId, despatchStatus, despatchSecurityClassification, despatchPrecedence, despatchFrom, despatchTo, despatchLetterNumber, despatchOriginatorNumber, despatchDate):
        self.despatchId = despatchId
        self.despatchStatus = despatchStatus
        self.despatchSecurityClassification = despatchSecurityClassification
        self.despatchPrecedence = despatchPrecedence
        self.despatchFrom = despatchFrom
        self.despatchTo = despatchTo
        self.despatchLetterNumber = despatchLetterNumber
        self.despatchOriginatorNumber = despatchOriginatorNumber
        self.despatchDate = despatchDate
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        despatchList = []
        for i in range(0, len(databaseResult)):
            despatchId = databaseResult[i][0]
            despatchStatus = databaseResult[i][1]
            despatchSecurityClassification = databaseResult[i][2]
            despatchPrecedence = databaseResult[i][3]
            despatchFrom = databaseResult[i][4]
            despatchTo = databaseResult[i][5]
            despatchLetterNumber = databaseResult[i][6]
            despatchOriginatorNumber = databaseResult[i][7]
            despatchDate = databaseResult[i][8]
            despatchList.append(Despatch(despatchId, despatchStatus, despatchSecurityClassification, despatchPrecedence, despatchFrom, despatchTo, despatchLetterNumber, despatchOriginatorNumber, despatchDate).__dict__)
        
        return despatchList
        