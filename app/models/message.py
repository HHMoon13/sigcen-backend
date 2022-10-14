import json
from app.general import util

class Message:
    
    def __init__(self, messageId, messagePrecedence, messageAction, messageDateTime, messageInstructions, messageSpecialInstructions,
                               messagePrefix, messageOriginatorsNumber, messageText, messageClassification, messageInfo, messageFrom, messageTo, messageSignRank, messageStatus):
        messageId = self.messageId
        messagePrecedence = self.messagePrecedence
        messageAction = self.messageAction
        messageDateTime = self.messageDateTime
        messageInstructions = self.messageInstructions
        messageSpecialInstructions = self.messageSpecialInstructions
        messagePrefix = self.messagePrefix
        messageOriginatorsNumber = self.messageOriginatorsNumber
        messageText = self.messageText
        messageClassification = self.messageClassification
        messageInfo = self.messageInfo
        messageFrom = self.messageFrom
        messageTo = self.messageTo
        messageSignRank = self.messageSignRank
        messageStatus = self.messageStatus
        
    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        messageList = []
        for i in range(0, len(databaseResult)):
            messageId = databaseResult[i][0]
            messagePrecedence = databaseResult[i][1]
            messageAction = databaseResult[i][2]
            messageDateTime = databaseResult[i][3]
            messageInstructions = databaseResult[i][4]
            messageSpecialInstructions = databaseResult[i][5]
            messagePrefix = databaseResult[i][6]
            messageOriginatorsNumber = databaseResult[i][7]
            messageText = databaseResult[i][8]
            messageClassification = databaseResult[i][9]
            messageInfo = databaseResult[i][10]
            messageFrom = databaseResult[i][11]
            messageTo = databaseResult[i][12]
            messageSignRank = databaseResult[i][13]
            messageStatus = databaseResult[i][14]
            messageList.append(Message(messageId, messagePrecedence, messageAction, messageDateTime, messageInstructions, messageSpecialInstructions,
                                    messagePrefix, messageOriginatorsNumber, messageText, messageClassification, messageInfo, messageFrom, messageTo, messageSignRank, messageStatus).__dict__)
        
        return messageList
        databaseResult[i][0]