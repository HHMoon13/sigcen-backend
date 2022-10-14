from flask_bcrypt import generate_password_hash, check_password_hash
from app.general.util import getdbconection, executesql, generateID, getObjectFromBinaryDecode, decodeJson
from app.general.constants import ServerEnum
from flask import jsonify, current_app, g
import click

from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.despatch import Despatch
from app.models.message import Message
from app.models.transit_slip import TransitSlip
from app.models.exercise import Exercise
from app.models.syndicate import Syndicate
from app.models.message import Message
from app.models.question import Question
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('teacher', __name__)

def loginTeacher(teacherEmail, teacherPassword):
    try:        
        teacher_data = executesql(query="SELECT * FROM teacher_table WHERE teacherEmail = ?",
                                  datatuple=[teacherEmail])
        
        if teacher_data and check_password_hash(teacher_data[0][3], teacherPassword):
            teacher_data = Teacher.toJsonMapListFromDatabase(teacher_data)

            return jsonify({
                'user': teacher_data,
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
        print("ERROR IN login_teacher() method in controllers/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
    
    
@bp.route('/teacher_add_exercise', methods=['POST'])
def addExercise():
    try:
        requestBody = request.json
        exerciseId = generateID('EXERCISE')
        courseId = requestBody['courseId']
        exerciseName = requestBody['exerciseName']
        exerciseDetails = requestBody['exerciseDetails']
        
        executesql(query="INSERT INTO exercise_table "
                            "(exerciseId, exerciseName, courseId, exerciseDetails)"
                            "values (?, ?, ?, ?)",
                    datatuple=[exerciseId, exerciseName, courseId, exerciseDetails])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addExercise() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/teacher_delete_exercise', methods=['POST'])
def deleteExercise():
    try:
        requestBody = request.json
        exerciseId = requestBody['exerciseId']
        
        executesql(query="DELETE FROM exercise_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])
        
        executesql(query="DELETE FROM course_exercise_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])
        
        executesql(query="DELETE FROM syndicate_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])

        executesql(query="DELETE FROM syndicate_exercise_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])
        
        executesql(query="DELETE FROM course_exercise_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])
        
        executesql(query="DELETE FROM question_association_table "
                            "WHERE exerciseId = ?",
                    datatuple=[exerciseId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteExercise() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/teacher_add_syndicate', methods=['POST'])
def addSyndicate():
    try:
        requestBody = request.json
        syndicateId = generateID('SYNDICATE')
        exerciseId = requestBody['exerciseId']
        syndicateName = requestBody['syndicateName']
        
        executesql(query="INSERT INTO syndicate_table "
                            "(syndicateId, exerciseId, syndicateName)"
                            "values (?, ?, ?)",
                    datatuple=[syndicateId, exerciseId, syndicateName])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addSyndicate() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/teacher_delete_syndicate', methods=['POST'])
def deleteSyndicate():
    try:
        requestBody = request.json
        syndicateId = requestBody['syndicateId']
        
        executesql(query="DELETE FROM syndicate_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM syndicate_members "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM syndicate_exercise_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM despatch_association_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM message_association_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM transit_slip_association_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
        
        executesql(query="DELETE FROM assignment_table "
                            "WHERE syndicateId = ?",
                    datatuple=[syndicateId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteSyndicate() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })



@bp.route('/teacher_add_student_to_syndicate', methods=['POST'])
def addStudentToSyndicate():
    try:
        requestBody = request.json
        syndicateId = requestBody['syndicateId']
        studentId = requestBody['studentId']
        studentRole = requestBody['studentRole']
        
        executesql(query="INSERT INTO syndicate_members "
                            "(syndicateId, studentId, studentRole)"
                            "values (?, ?, ?)",
                    datatuple=[syndicateId, studentId, studentRole])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addStudentToSyndicate() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        

@bp.route('/teacher_add_syndicate_to_exercise', methods=['POST'])
def addSyndicateToExercise():
    try:
        requestBody = request.json
        syndicateId = requestBody['syndicateId']
        exerciseId = requestBody['exerciseId']
        

        executesql(query="INSERT INTO syndicate_exerise_table "
                            "(syndicateId, exerciseId)"
                            "values (?, ?)",
                    datatuple=[syndicateId, exerciseId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addSyndicateToExercise() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        

@bp.route('/teacher_create_despatch', methods=['POST'])
def createDespatch():
    try:
        requestBody = request.json
        despatchId = generateID('DESPATCH')
        despatchStatus = "NEW"
        despatchSecurityClassification = requestBody['despatchSecurityClassification']
        despatchPrecedence = requestBody['despatchPrecedence']
        despatchFrom = requestBody['despatchFrom']
        despatchTo = requestBody['despatchTo']
        despatchLetterNumber = requestBody['despatchLetterNumber']
        despatchOriginatorNumber = requestBody['despatchOriginatorNumber']
        despatchDate = requestBody['despatchDate']
        
        teacherId = requestBody['teacherId']
        studentId = requestBody['studentId']
        syndicateId = requestBody['syndicateId']
                
        executesql(query="INSERT INTO despatch_table "
                            "(despatchId, despatchStatus, despatchSecurityClassification, despatchPrecedence, despatchFrom, despatchTo, despatchLetterNumber, despatchOriginatorNumber, despatchDate)"
                            "values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    datatuple=[despatchId, despatchStatus, despatchSecurityClassification, despatchPrecedence, despatchFrom, despatchTo, despatchLetterNumber, despatchOriginatorNumber, despatchDate])
                    
        executesql(query="INSERT INTO despatch_association_table "
                            "(despatchId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[despatchId, syndicateId, teacherId])
        
        executesql(query="INSERT INTO despatch_association_table "
                            "(despatchId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[despatchId, syndicateId, studentId])
        
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN createDespatch() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/teacher_delete_despatch', methods=['POST'])
def deleteDespatch():
    try:
        requestBody = request.json

        despatchId = requestBody['despatchId']
                
        executesql(query="DELETE FROM despatch_table "
                            "WHERE despatchId = ?",
                    datatuple=[despatchId])
        
        executesql(query="DELETE FROM despatch_association_table "
                            "WHERE despatchId = ?",
                    datatuple=[despatchId])
        
        executesql(query="DELETE FROM assignment_table "
                            "WHERE despatchId = ?",
                    datatuple=[despatchId])
        
        executesql(query="DELETE FROM transit_slip_association_table "
                            "WHERE despatchId = ?",
                    datatuple=[despatchId])
        
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteDespatch() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        

@bp.route('/teacher_get_syndicate_members', methods=['POST'])
def getSyndicateMembers():
    try:       
        requestBody = request.json
        syndicateId = requestBody['syndicateId'] 

        syndicateList = executesql("SELECT a.studentRole, b.studentName, b.studentEmail, b.studentId FROM syndicate_members AS a INNER JOIN student_table AS b ON a.studentId = b.studentId WHERE a.syndicateId = ?",
                                          datatuple=[syndicateId])
        
        syndicateData = []
        
        for i in range(0, len(syndicateList)):
            syndicateData.append({'studentRole': syndicateList[i][0], 'studentName': syndicateList[i][1], 'studentEmail': syndicateList[i][2], 'studentId': syndicateList[i][3]})
        
        return jsonify({
                'syndicateData': syndicateData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getSyndicateMembers() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
        
@bp.route('/teacher_get_despatch', methods=['POST'])
def getDespatches():
    try:
        requestBody = request.json
        teacherId = requestBody['teacherId']
        despatchData = Despatch.toJsonMapListFromDatabase(executesql(query="SELECT d.despatchId, d.despatchStatus, " 
                                                                     "d.despatchSecurityClassification, d.despatchPrecedence, d.despatchFrom, d.despatchTo, "
                                                                     "d.despatchLetterNumber, d.despatchOriginatorNumber, d.despatchDate from despatch_table as d "
                                                                     "INNER JOIN despatch_association_table as a ON d.despatchId = a.despatchId WHERE a.associationId = ?",
                                                                    datatuple=[teacherId]))
          
        return jsonify({
                'despatchData': despatchData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAllDespatches() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/teacher_get_all_messages')
def getAllMessages():
    try:
        messageData = Message.toJsonMapListFromDatabase(executesql(query="SELECT * from message_table",
                    datatuple=[]))
        
        return jsonify({
                'messageData': messageData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAllMessages() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        

@bp.route('/teacher_get_syndicate', methods=['POST'])
def getSyndicateList():
    try:
        requestBody = request.json
        
        exerciseId = requestBody['exerciseId']
        syndicateData = Syndicate.toJsonMapListFromDatabase(executesql(query="SELECT * from syndicate_table WHERE exerciseId = ?",
                    datatuple=[exerciseId]))
        
        return jsonify({
                'syndicateData': syndicateData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getSyndicateList() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/teacher_get_all_students')
def getAllStudents():
    try:

        studentData = Student.toJsonMapListFromDatabase(executesql(query="SELECT * from student_table",
                    datatuple=[]))
        
        return jsonify({
                'studentList': studentData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAllStudents() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        

@bp.route('/teacher_get_all_courses')
def getAllCourse():
    try:
        courseData = Course.toJsonMapListFromDatabase(executesql(query="SELECT * from course_table",
                    datatuple=[]))
        
        return jsonify({
                'courseList': courseData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAllCourse() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/teacher_get_course_exercises', methods=['POST'])
def getAllExercise():
    try:
        requestBody = request.json
        courseId = requestBody['courseId']
        exerciseData = Exercise.toJsonMapListFromDatabase(executesql(query="SELECT * from exercise_table WHERE courseId = ?",
                    datatuple=[courseId]))
        
        return jsonify({
                'exerciseList': exerciseData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAllExercise() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
@bp.route('/teacher_get_teacher_courses', methods=['POST'])
def getTeacherCourses():
    try:       
        requestBody = request.json
        teacherId = requestBody['teacherId'] 
        

        teacherCourseList = executesql("SELECT c.courseId, c.courseName FROM course_table AS c INNER JOIN teacher_table AS t ON c.madeBy = t.teacherId WHERE t.teacherId = ?",
                                          datatuple=[teacherId])

        teacherCourseData = []
        
        for i in range(0, len(teacherCourseList)):
            teacherCourseData.append({'courseId': teacherCourseList[i][0], 'courseName': teacherCourseList[i][1]})
        
        return jsonify({
                'teacherCourseData': teacherCourseData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getTeacherCourses() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/teacher_get_course_students', methods=['POST'])
def getCourseStudent():
    try:       
        requestBody = request.json
        courseId = requestBody['courseId'] 

        courseStudentList = executesql("SELECT s.studentId, s.studentName, s.studentEmail, s.studentPhone from takes_table as t INNER JOIN student_table as s ON s.studentId = t.studentId WHERE t.courseId = ?",
                                          datatuple=[courseId])
        
        courseStudentData = []
        
        for i in range(0, len(courseStudentList)):
            courseStudentData.append({'studentId': courseStudentList[i][0], 'studentName': courseStudentList[i][1],
                                      'studentEmail':courseStudentList[i][2], 'studentPhone':courseStudentList[i][3]})
        
        return jsonify({
                'courseStudentData': courseStudentData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getCourseStudent() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})

@bp.route('/get_register', methods=['GET'])
def getRegister():
    try:
        messageStatus = "ACCEPTED"
        messageDataRaw = executesql(query="SELECT * from message_table "
                                        "WHERE messageStatus=?",
                                        datatuple=[messageStatus])
        
        registerData = []
        for i in range(0, len(messageDataRaw)):
            registerData.append({'messageId': messageDataRaw[i][0], 'messagePrecedence': messageDataRaw[i][1], 'messageAction': messageDataRaw[i][2],
                                 'messageDateTime': messageDataRaw[i][3], 'messageInstructions': messageDataRaw[i][4], 'messageSpecialInstructions': messageDataRaw[i][5],
                                 'messagePrefix': messageDataRaw[i][6], 'messageOriginatorsNumber': messageDataRaw[i][7], 'messageText': messageDataRaw[i][8],   
                                 'messageClassification': messageDataRaw[i][9], 'messageInfo': messageDataRaw[i][10], 'messageFrom': messageDataRaw[i][11],
                                 'messageTo': messageDataRaw[i][12], 'messageSignRank': messageDataRaw[i][13], 'messageStatus': messageDataRaw[i][14]})
        
        return jsonify({
                'registerData': registerData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getRegister() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/teacher_get_transit_slip', methods=['GET'])
def getteacherTransitSlip():
    try:       
        
        transitSlipData = TransitSlip.toJsonMapListFromDatabase(executesql("SELECT * from transit_slip_table",
                                                            datatuple=[]))        
        
        return jsonify({
                'transitSlipData': transitSlipData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getteacherTransitSlip() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})

    
@bp.route('/teacher_add_transit_slip', methods=['POST'])
def addTransitSlip():
    try:
        requestBody = request.json
        transitSlipId = generateID('TRANSITSLIP')
        transitSlipFrom = requestBody['transitSlipFrom']
        transitSlipTo = requestBody['transitSlipTo']
        transitSlipRoute = requestBody['transitSlipRoute']
        transitSlipCourier = requestBody['transitSlipCourier']
        
        executesql(query="INSERT INTO transit_slip_table "
                            "(transitSlipId, transitSlipFrom, transitSlipTo, transitSlipRoute, transitSlipCourier)"
                            "values (?, ?, ?, ?, ?)",
                    datatuple=[transitSlipId, transitSlipFrom, transitSlipTo, transitSlipRoute, transitSlipCourier])
        
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addTransitSlip() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
    
@bp.route('/teacher_delete_transit_slip', methods=['POST'])
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
        print("ERROR IN deleteTransitSlip() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
            
@bp.route('/create_message', methods=['POST'])
def createMessage():
    try:
        requestBody = request.json
        
        syndicateId = requestBody['syndicateId']
        teacherId = requestBody['teacherId']
        studentId = requestBody['studentId']
        
        messageId = generateID('MESSAGE')
        messagePrecedence = requestBody['messagePrecedence']
        messageAction = requestBody['messageAction']
        messageDateTime = requestBody['messageDateTime']
        messageInstructions = requestBody['messageInstructions']
        messageSpecialInstructions = requestBody['messageSpecialInstructions']
        messagePrefix = requestBody['messagePrefix']
        messageOriginatorsNumber = requestBody['messageOriginatorsNumber']
        messageText = requestBody['messageText']
        messageClassification = requestBody['messageClassification']
        messageInfo = requestBody['messageInfo']
        messageFrom = requestBody['messageFrom']
        messageTo = requestBody['messageTo']
        messageSignRank = requestBody['messageSignRank']
        messageStatus = "NEW"

        executesql(query="INSERT INTO message_table "
                            "(messageId, messagePrecedence, messageAction, "
                            "messageDateTime, messageInstructions, messageSpecialInstructions, messagePrefix, "
                            "messageOriginatorsNumber, messageText, messageClassification, messageInfo, messageFrom, "
                            "messageTo, messageSignRank, messageStatus) "
                            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    datatuple=[messageId, messagePrecedence, messageAction, messageDateTime, messageInstructions, messageSpecialInstructions,
                               messagePrefix, messageOriginatorsNumber, messageText, messageClassification, messageInfo, messageFrom, messageTo, messageSignRank, messageStatus])
                    
        executesql(query="INSERT INTO message_association_table "
                            "(messageId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[messageId, syndicateId, teacherId])    
        
        executesql(query="INSERT INTO message_association_table "
                            "(messageId, syndicateId, associationId)"
                            "values (?, ?, ?)",
                    datatuple=[messageId, syndicateId, studentId])    
           
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN createMessage() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        

@bp.route('/delete_message', methods=['POST'])
def deleteMessage():
    try:
        requestBody = request.json

        messageId = requestBody['messageId']

        executesql(query="DELETE FROM message_association_table "
                            "WHERE messageId = ?",
                    datatuple=[messageId])
        
        executesql(query="DELETE FROM assignment_table "
                            "WHERE messageId = ?",
                    datatuple=[messageId])
        
        executesql(query="DELETE FROM message_table "
                            "WHERE messageId = ?",
                    datatuple=[messageId])
           
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteMessage() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        

@bp.route('/teacher_get_messages', methods=['POST'])
def getMessages():
    try:
        requestBody = request.json
        teacherId = requestBody['teacherId']
        messageDataRaw = executesql(query="SELECT m.messageId, m.messagePrecedence, m.messageAction, m.messageDateTime, "
                                                                   "m.messageInstructions, m.messageSpecialInstructions, m.messagePrefix, m.messageOriginatorsNumber, "
                                                                   "m.messageText, m.messageClassification, m.messageInfo, m.messageFrom, m.messageTo, "
                                                                   "m.messageSignRank, m.messageStatus from message_table as m "
                                                                    "INNER JOIN message_association_table as a ON m.messageId = a.messageId WHERE a.associationId = ?",
                                                                    datatuple=[teacherId])
        
        messageData = []
        for i in range(0, len(messageDataRaw)):
            messageData.append({'messageId': messageDataRaw[i][0], 'messagePrecedence': messageDataRaw[i][1], 'messageAction': messageDataRaw[i][2],
                                 'messageDateTime': messageDataRaw[i][3], 'messageInstructions': messageDataRaw[i][4], 'messageSpecialInstructions': messageDataRaw[i][5],
                                 'messagePrefix': messageDataRaw[i][6], 'messageOriginatorsNumber': messageDataRaw[i][7], 'messageText': messageDataRaw[i][8],   
                                 'messageClassification': messageDataRaw[i][9], 'messageInfo': messageDataRaw[i][10], 'messageFrom': messageDataRaw[i][11],
                                 'messageTo': messageDataRaw[i][12], 'messageSignRank': messageDataRaw[i][13], 'messageStatus': messageDataRaw[i][14]})
          
        return jsonify({
                'messageData': messageData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getMessages() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
        
@bp.route('/teacher_upload_question', methods=['POST'])
def uploadquestion():
    try:
        requestBody = request.json
        exerciseId = requestBody['exerciseId']
        teacherId = requestBody['teacherId']
        
        questionId = generateID('QUESTION') 
        questionTitle = requestBody['questionTitle']
        questionGeneralIdea = requestBody['questionGeneralIdea']
        questionSpecialIdea = requestBody['questionSpecialIdea']
        questionNarrative1 = requestBody['questionNarrative1']
        questionRequirement1 = requestBody['questionRequirement1']
        questionNarrative2 = requestBody['questionNarrative2']
        questionRequirement2 = requestBody['questionRequirement2']
        
        
        
        executesql(query="INSERT INTO question_table "
                            "(questionId, questionTitle, questionGeneralIdea, "
                            "questionSpecialIdea, questionNarrative1, questionRequirement1, "
                            "questionNarrative2, questionRequirement2)"
                            "values (?, ?, ?, ?, ?, ?, ?, ?)",
                    datatuple=[questionId, questionTitle, questionGeneralIdea, 
                               questionSpecialIdea, questionNarrative1, questionRequirement1, 
                               questionNarrative2, questionRequirement2])
        
        executesql(query="INSERT INTO question_association_table "
                            "(questionId, exerciseId, teacherId, "
                            "values (?, ?, ?)",
                    datatuple=[questionId, exerciseId, teacherId])
                    
          
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN uploadquestion() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
        
@bp.route('/teacher_delete_question', methods=['POST'])
def deletequestion():
    try:
        requestBody = request.json
        questionId = requestBody['questionId']
        
        executesql(query="DELETE FROM question_association_table "
                            "WHERE questionId = ?",
                    datatuple=[questionId])
        
        executesql(query="DELETE FROM question_table "
                            "WHERE questionId = ?",
                    datatuple=[questionId])
          
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deletequestion() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
@bp.route('/teacher_get_question', methods=['POST'])
def teacherGetQuestions():
    try:
        requestBody = request.json
        teacherId = requestBody['teacherId']
        
        questionList = Question.toJsonMapListFromDatabase(executesql(query="SELECT q.questionId, q.questionTitle, q.questionGeneralIdea, "
                                                    "q.questionSpecialIdea, q.questionNarrative1, q.questionRequirement1, "
                                                    "q.questionNarrative2, q.questionRequirement2 FROM question_table as q "
                                                    "INNER JOIN question_association_table as a ON a.questionId = q.questionId "
                                                    "WHERE a.teacherId = ?",
                                                datatuple=[teacherId]))
                     
        return jsonify({
                "questionList": questionList, 
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN teacherGetQuestions() method in views/teacher.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
        
