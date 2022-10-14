import json
from app.general import util

class Admin:
    
    def __init__(self, adminId, adminEmail, adminName, adminPhone):
        self.adminId = adminId
        self.adminEmail = adminEmail
        self.adminName = adminName
        self.adminPhone = adminPhone
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        adminList = []
        for i in range(0, len(databaseResult)):
            adminId = databaseResult[i][0]
            adminEmail = databaseResult[i][1]
            adminName = databaseResult[i][2]
            #adminPassword = databaseResult[i][3]
            adminPhone = databaseResult[i][4]
            adminList.append(Admin(adminId, adminEmail, adminName, adminPhone).__dict__)
        
        return adminList
        
        # despatchId, despatchName, despatchDetails, despatchStatus
        
        # association: despId, associationId, syndicateId
        
        # transit slip: transitSlipId, 
        
        # transit_despatch_table: 