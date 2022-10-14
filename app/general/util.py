import app.database as database
import json
import uuid
import ast

def getObjectFromBinaryDecode(VALUE):
    if VALUE is not None:
        return ast.literal_eval(VALUE.decode())
    else:
        return None

def decodeJson(requestBody):
    bodyUnicode = requestBody.decode('utf-8')
    body = json.loads(bodyUnicode)
    return body

def executesql(query, datatuple):
    db = getdbconection()
    cursor = db.cursor()
    cursor.execute(query, datatuple)
    databaseResult = cursor.fetchall()
    if len(datatuple) != 0: db.commit()
    cursor.close()
    return databaseResult

def generateID(prefix):
    uuID = prefix + "_" + str(uuid.uuid4())
    randomUUID = uuID.replace('-', '_')
    return randomUUID


def getdbconection():
    db = database.get_db()
    return db