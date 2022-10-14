from flask_bcrypt import generate_password_hash, check_password_hash
from app.general.util import getdbconection, executesql
from app.general.constants import ServerEnum
from flask import jsonify, current_app, g
import click
import functools
from app.general.util import getdbconection, executesql, generateID, getObjectFromBinaryDecode, decodeJson
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.despatch import Despatch
from app.models.message import Message
from app.models.transit_slip import TransitSlip
from app.models.exercise import Exercise
from app.models.syndicate import Syndicate
from app.models.question import Question

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('student', __name__)

def loginStudent(studentEmail, studentPassword):
    try:        
        student_data = executesql(query="SELECT * FROM student_table WHERE studentEmail = ?",
                                  datatuple=[studentEmail])
        
        if student_data and check_password_hash(student_data[0][3], studentPassword):
            student_data = Student.toJsonMapListFromDatabase(student_data)

            return jsonify({
                # 'authCredential': authCredential,
                'user': student_data,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
        else:
            return jsonify({
                'message': "No such user",
                'status': False,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
            
    except Exception as e:
        print("ERROR IN login_student() method in controllers/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/student_assign_despatch', methods=['POST'])
def assignDespatch():
    try:
        requestBody = request.json
        despatchId = requestBody['despatchId']
        syndicateId = requestBody['syndicateId']
        studentId = requestBody['studentId']
        

        executesql(query="INSERT INTO despatch_association_table "
                            "(despatchId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[despatchId, syndicateId, studentId])
        
        executesql(query="UPDATE despatch_table SET "
                                        "despatchStatus = ?"
                                        "WHERE despatchId = ?",
                                    datatuple=["PENDING", despatchId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN assignDespatch() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
        
@bp.route('/student_get_courses', methods=['POST'])
def getCourseStudent():
    try:       
        requestBody = request.json
        studentId = requestBody['studentId'] 

        courseList = executesql("SELECT c.courseId, c.courseName FROM course_table AS c INNER JOIN takes_table AS t ON c.courseId = t.courseId WHERE t.studentId = ?",
                                          datatuple=[studentId])
        
        courseData = []
        
        for i in range(0, len(courseList)):
            courseData.append({'courseId': courseList[i][0], 'courseName': courseList[i][1]})
        
        return jsonify({
                'courseData': courseData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getCourseStudent() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/student_get_despatches', methods=['POST'])
def studentGetDespatches():
    try:
        requestBody = request.json
    
        studentId = requestBody['studentId']
        despatchData = []
        despatchDataRaw = executesql(query="SELECT d.despatchId, d.despatchStatus, " 
                            "d.despatchSecurityClassification, d.despatchPrecedence, d.despatchFrom, d.despatchTo, "
                            "d.despatchLetterNumber, d.despatchOriginatorNumber, d.despatchDate, a.syndicateId, s.studentRole from despatch_table as d "
                            "INNER JOIN despatch_association_table as a ON d.despatchId = a.despatchId "
                            "INNER JOIN syndicate_members as s ON a.associationId = s.studentId AND a.syndicateId = s.syndicateId "
                            "WHERE a.associationId = ?",
                              datatuple=[studentId])
                
        for i in range(0, len(despatchDataRaw)):
            despatchData.append({'despatchId': despatchDataRaw[i][0], 'despatchStatus': despatchDataRaw[i][1], 'despatchSecurityClassification': despatchDataRaw[i][2],
                                 'despatchPrecedence': despatchDataRaw[i][3], 'despatchFrom': despatchDataRaw[i][4], 'despatchTo': despatchDataRaw[i][5],
                                 'despatchLetterNumber': despatchDataRaw[i][6], 'despatchOriginatorNumber': despatchDataRaw[i][7], 'despatchDate': despatchDataRaw[i][8],   
                                 'syndicateId': despatchDataRaw[i][9], 'studentRole': despatchDataRaw[i][10]})
            
          
        return jsonify({
                'despatchData': despatchData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN studentGetDespatches() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        

@bp.route('/create_transit_slip', methods=['POST'])
def createTransitSlip():
    try:
        requestBody = request.json
        transitSlipId = generateID('TRANSITSLIP')
        transitSlipFrom = requestBody['transitSlipFrom']
        transitSlipTo = requestBody['transitSlipTo']
        transitSlipRoute = requestBody['transitSlipRoute']
        transitSlipCourier = requestBody['transitSlipCourier']
        transitSlipNumber = requestBody['transitSlipNumber']

        executesql(query="INSERT INTO transit_slip_table "
                            "(transitSlipId, transitSlipFrom, transitSlipTo, "
                            "transitSlipRoute, transitSlipCourier, transitSlipStatus, transitSlipNumber)"
                            "values (?, ?, ?, ?, ?, ?, ?)",
                    datatuple=[transitSlipId, transitSlipFrom, transitSlipTo, 
                               transitSlipRoute, transitSlipCourier, "NEW", transitSlipNumber])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN createTransitSlip() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
        
@bp.route('/student_delete_transit_slip', methods=['POST'])
def deleteTransitSlip():
    try:
        requestBody = request.json
        transitSlipId = requestBody['transitSlipId']
        
        executesql(query="DELETE FROM transit_slip_table "
                            "WHERE transitSlipId = ?",
                    datatuple=[transitSlipId])
        
        executesql(query="DELETE FROM transit_slip_association_table "
                            "WHERE transitSlipId = ?",
                    datatuple=[transitSlipId])
        
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteTransitSlip() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/student_get_new_transit_slip', methods=['POST'])
def getNewTransitSip():
    try:
        
        data = TransitSlip.toJsonMapListFromDatabase(executesql(query="SELECT * FROM transit_slip_table WHERE transitSlipStatus = ?",
                    datatuple=["NEW"]))
                    
        return jsonify({
                "transitSlipData": data,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getNewTransitSip() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/student_add_despatch_to_transit_slip',  methods=['POST'])
def addDespatchToTransitSlip():
    try:
        requestBody = request.json
        transitSlipId = requestBody['transitSlipId']
        despatchId = requestBody['despatchId']
        syndicateId = requestBody['syndicateId']

        executesql(query="INSERT INTO transit_slip_association_table "
                            "(transitSlipId, despatchId, syndicateId)"
                            "values (?, ?, ?)",
                    datatuple=[transitSlipId, despatchId, syndicateId])
        
        executesql(query="UPDATE despatch_table SET "
                                        "despatchStatus = ?"
                                        "WHERE despatchId = ?",
                                    datatuple=["ADDED", despatchId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addDespatchToTransitSlip() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/student_get_transit_slips', methods=['POST'])
def getTransitSlips():
    try:
        requestBody = request.json
    
        studentId = requestBody['studentId']
        transitSlipRaw = executesql(query="SELECT DISTINCT s.syndicateId, s.studentRole, t.transitSlipId, t.transitSlipFrom, t.transitSlipTo, "
                                    "t.transitSlipNumber, t.transitSlipRoute, t.transitSlipCourier, t.transitSlipStatus "
                                    "FROM syndicate_members as s "
                                    "INNER JOIN transit_slip_association_table as ta ON s.syndicateId = ta.syndicateId "
                                    "INNER JOIN transit_slip_table as t ON ta.transitSlipId = t.transitSlipId "
                                    "WHERE s.studentId = ?",
                              datatuple=[studentId]) 
        transitSlipData = []
                
        for i in range(0, len(transitSlipRaw)):
            transitSlipData.append({'syndicateId': transitSlipRaw[i][0], 'studentRole': transitSlipRaw[i][1], 
                                    'transitSlipId': transitSlipRaw[i][2], 'transitSlipFrom': transitSlipRaw[i][3],
                                 'transitSlipTo': transitSlipRaw[i][4], 'transitSlipNumber': transitSlipRaw[i][5], 'transitSlipRoute': transitSlipRaw[i][6],
                                 'transitSlipCourier': transitSlipRaw[i][7], 'transitSlipStatus': transitSlipRaw[i][8]})
            
          
        return jsonify({
                'transitSlipData': transitSlipData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN studentGetDespatches() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})

@bp.route('/student_update_transit_slip', methods=['POST'])
def updateTransitSlip():
    try:
        requestBody = request.json
        transitSlipId = requestBody['transitSlipId']
        transitSlipStatus = requestBody['transitSlipStatus']

        executesql(query="UPDATE transit_slip_table SET "
                                        "transitSlipStatus = ?"
                                        "WHERE transitSlipId = ?",
                                    datatuple=[transitSlipStatus, transitSlipId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN updateTransitSlip() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/student_get_transit_slip_despatches', methods=['POST'])
def studentGetTransitSlipDespatches():
    try:
        requestBody = request.json
    
        transitSlipId = requestBody['transitSlipId']
        despatchData = []
        despatchDataRaw = executesql(query="SELECT d.despatchId, d.despatchStatus, " 
                            "d.despatchSecurityClassification, d.despatchPrecedence, d.despatchFrom, d.despatchTo, "
                            "d.despatchLetterNumber, d.despatchOriginatorNumber, d.despatchDate from despatch_table as d "
                            "INNER JOIN transit_slip_association_table as a ON d.despatchId = a.despatchId "
                            "WHERE a.transitSlipId = ?",
                              datatuple=[transitSlipId])
                
        for i in range(0, len(despatchDataRaw)):
            despatchData.append({'despatchId': despatchDataRaw[i][0], 'despatchStatus': despatchDataRaw[i][1], 'despatchSecurityClassification': despatchDataRaw[i][2],
                                 'despatchPrecedence': despatchDataRaw[i][3], 'despatchFrom': despatchDataRaw[i][4], 'despatchTo': despatchDataRaw[i][5],
                                 'despatchLetterNumber': despatchDataRaw[i][6], 'despatchOriginatorNumber': despatchDataRaw[i][7], 'despatchDate': despatchDataRaw[i][8]
                                 })
            
          
        return jsonify({
                'despatchData': despatchData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN studentGetTransitSlipDespatches() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/student_update_message', methods=['POST'])
def updateMessage():
    try:
        requestBody = request.json
        messageId = requestBody['messageId']
        messageStatus = requestBody['messageStatus']
        

        executesql(query="UPDATE message_table SET "
                                        "messageStatus = ?"
                                        "WHERE messageId = ?",
                                    datatuple=[messageStatus, messageId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN updateMessage() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/student_get_messages', methods=['POST'])
def getMessages():
    try:
        requestBody = request.json
    
        studentId = requestBody['studentId']
        messageData = []
        messageDataRaw = executesql(query="SELECT DISTINCT m.messageId, m.messagePrecedence, m.messageAction, m.messageDateTime, "
                                    "m.messageInstructions, m.messageSpecialInstructions, m.messagePrefix, m.messageOriginatorsNumber, "
                                    "m.messageText, m.messageClassification, m.messageInfo, m.messageFrom, m.messageTo, "
                                    "m.messageSignRank, m.messageStatus, a.syndicateId, s.studentRole from message_table as m "
                                    "INNER JOIN message_association_table as a ON m.messageId = a.messageId "
                                    "INNER JOIN syndicate_members as s ON a.associationId = s.studentId AND a.syndicateId = s.syndicateId "
                                    "WHERE a.associationId = ?",
                                    datatuple=[studentId])
                
        for i in range(0, len(messageDataRaw)):
            messageData.append({'messageId': messageDataRaw[i][0], 'messagePrecedence': messageDataRaw[i][1], 'messageAction': messageDataRaw[i][2],
                                 'messageDateTime': messageDataRaw[i][3], 'messageInstructions': messageDataRaw[i][4], 'messageSpecialInstructions': messageDataRaw[i][5],
                                 'messagePrefix': messageDataRaw[i][6], 'messageOriginatorsNumber': messageDataRaw[i][7], 'messageText': messageDataRaw[i][8],   
                                 'messageClassification': messageDataRaw[i][9], 'messageInfo': messageDataRaw[i][10], 'messageFrom': messageDataRaw[i][11],
                                 'messageTo': messageDataRaw[i][12], 'messageSignRank': messageDataRaw[i][13], 'messageStatus': messageDataRaw[i][14],
                                 'syndicateId': messageDataRaw[i][15], 'studentRole': messageDataRaw[i][16]})
            
          
        return jsonify({
                'messageData': messageData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getMessages() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/student_assign_message', methods=['POST'])
def assignMessage():
    try:
        requestBody = request.json
        messageId = requestBody['messageId']
        syndicateId = requestBody['syndicateId']
        studentId = requestBody['studentId']
        

        executesql(query="INSERT INTO message_association_table "
                            "(messageId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[messageId, syndicateId, studentId])
        
        executesql(query="UPDATE message_table SET "
                                        "messageStatus = ?"
                                        "WHERE messageId = ?",
                                    datatuple=["PENDING", messageId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN assignMessage() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/student_get_question', methods=['POST'])
def studentGetQuestions():
    try:
        requestBody = request.json
        exerciseId = requestBody['exerciseId']
        
        questionList = Question.toJsonMapListFromDatabase(executesql(query="SELECT q.questionId, q.questionTitle, q.questionGeneralIdea, "
                                                    "q.questionSpecialIdea, q.questionNarrative1, q.questionRequirement1, "
                                                    "q.questionNarrative2, q.questionRequirement2 FROM question_table as q "
                                                    "INNER JOIN question_association_table as a ON a.questionId = q.questionId "
                                                    "WHERE a.exerciseId = ?",
                                                datatuple=[exerciseId]))
                     
        return jsonify({
                "questionList": questionList, 
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN studentGetQuestions() method in views/student.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})