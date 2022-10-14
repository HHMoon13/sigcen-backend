import json
from app.general import util

class TransitSlip:
    def __init__(self, transitSlipId, transitSlipFrom, transitSlipTo, transitSlipNumber, transitSlipRoute, transitSlipCourier, transitSlipStatus):
        self.transitSlipId = transitSlipId
        self.transitSlipFrom = transitSlipFrom
        self.transitSlipTo = transitSlipTo
        self.transitSlipNumber = transitSlipNumber
        self.transitSlipRoute = transitSlipRoute 
        self.transitSlipCourier = transitSlipCourier
        self.transitSlipStatus = transitSlipStatus
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        transitSlipList = []
        for i in range(0, len(databaseResult)):
            transitSlipId = databaseResult[i][0]
            transitSlipFrom = databaseResult[i][1]
            transitSlipTo = databaseResult[i][2] 
            transitSlipNumber = databaseResult[i][3] 
            transitSlipRoute = databaseResult[i][4] 
            transitSlipCourier = databaseResult[i][5] 
            transitSlipStatus = databaseResult[i][6] 
            transitSlipList.append(TransitSlip(transitSlipId, transitSlipFrom, transitSlipTo, transitSlipNumber, transitSlipRoute, transitSlipCourier, transitSlipStatus).__dict__)
        
        return transitSlipList
        