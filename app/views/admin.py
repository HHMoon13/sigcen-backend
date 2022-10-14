from types import MethodType
from flask_bcrypt import generate_password_hash, check_password_hash
from app.general.util import getdbconection, executesql, generateID, getObjectFromBinaryDecode, decodeJson
from app.general.constants import ServerEnum
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.models.course import Course
from app.models.exercise import Exercise
from flask import jsonify, current_app, g
import click
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__)

def loginAdmin(adminEmail, adminPassword):
    try:        
        admin_data = executesql(query="SELECT * FROM admin_table WHERE adminEmail = ?",
                                  datatuple=[adminEmail])
        
        if admin_data and check_password_hash(admin_data[0][3], adminPassword):
            admin_data = Admin.toJsonMapListFromDatabase(admin_data)

            return jsonify({
                # 'authCredential': authCredential,
                'user': admin_data,
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
        print("ERROR IN loginAdmin() method in controllers/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
        
@bp.route('/get_admin')
def getAdmin():
    try:        
        adminData = Admin.toJsonMapListFromDatabase(executesql(query="SELECT * from admin_table",
                    datatuple=[]))
        
        return jsonify({
                'adminList': adminData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getAdmin() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})



@bp.route('/admin_test')
def testAdmin():
    try:
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN adminTest() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })

@bp.route('/add_admin', methods=['POST'])
def addAdmin():
    try:
        requestBody = request.json
        adminId = generateID('ADMIN')
        adminName = requestBody['adminName']
        adminEmail = requestBody['adminEmail']
        adminPhone = requestBody['adminPhone']
        adminPassword = requestBody['adminPassword']
        userDetails = requestBody['userDetails']
        
        executesql(query="INSERT INTO admin_table (adminId, adminName, adminEmail, adminPhone, adminPassword) values (?,?,?,?,?)",
                    datatuple=[adminId, adminName, adminEmail, adminPhone, adminPassword])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addAdmin() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/admin_add_course', methods=['POST'])
def addCourse():
    try:
        requestBody = request.json
        courseId = generateID('COURSE')
        courseName = requestBody['courseName']
        madeBy = requestBody['madeBy']
        # courseDetails = requestBody['courseDetails']
        
        executesql(query="INSERT INTO course_table "
                            "(courseId, courseName, madeBy)"
                            "values (?, ?, ?)",
                    datatuple=[courseId, courseName, madeBy])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addCourse() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
        
@bp.route('/admin_delete_course', methods=['POST'])
def deleteCourse():
    try:
        requestBody = request.json
        courseId = requestBody['courseId']
        
        executesql(query="DELETE FROM course_table "
                            "WHERE courseId = ?",
                    datatuple=[courseId])
        
        executesql(query="DELETE FROM exercise_table "
                            "WHERE courseId = ?",
                    datatuple=[courseId])
        
        executesql(query="DELETE FROM course_exercise_table "
                            "WHERE courseId = ?",
                    datatuple=[courseId])
        
        executesql(query="DELETE FROM takes_table "
                            "WHERE courseId = ?",
                    datatuple=[courseId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteCourse() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@bp.route('/admin_add_teacher', methods=['POST'])
def addTeacher():
    try:
        requestBody = request.json
        
        teacherId = generateID('TEACHER')
        teacherEmail = requestBody['teacherEmail']
        # encryptedPassword = generate_password_hash(requestBody['teacherPassword'])
        encryptedPassword = generate_password_hash('123456')
        teacherName = requestBody['teacherName']
        teacherPhone = requestBody['teacherPhone']
        # userDetails = getObjectFromBinaryDecode(requestBody['userDetails'])
        
        executesql(query="INSERT INTO teacher_table (teacherId, teacherEmail, teacherName, teacherPassword, teacherPhone) values (?, ?, ?, ?, ?)",
                    datatuple=[teacherId, teacherEmail, teacherName, encryptedPassword, teacherPhone])
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addTeacher() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
@bp.route('/admin_delete_teacher', methods=['POST'])
def deleteTeacher():
    try:
        requestBody = request.json
        
        teacherId = requestBody['teacherId']
        
        executesql(query="DELETE FROM teacher_table "
                            "WHERE teacherId = ?",
                    datatuple=[teacherId])
        
        executesql(query="DELETE FROM question_association_table "
                            "WHERE teacherId = ?",
                    datatuple=[teacherId])
        
        executesql(query="DELETE FROM despatch_association_table "
                            "WHERE associationId = ?",
                    datatuple=[teacherId])
        
        executesql(query="DELETE FROM message_association_table "
                            "WHERE associationId = ?",
                    datatuple=[teacherId])
                    
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN deleteTeacher() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/admin_add_student', methods=['POST'])
def addStudent():
    try:
        requestBody = request.json
        
        studentId = generateID('STUDENT')
        studentEmail = requestBody['studentEmail']
        studentName = requestBody['studentName']
        encryptedPassword = generate_password_hash('123456')
        # encryptedPassword = generate_password_hash(requestBody['studentPassword'])
        studentPhone = requestBody['studentPhone']
        # userDetails = getObjectFromBinaryDecode(requestBody['userDetails'])
        
        executesql(query="INSERT INTO student_table "
                            "(studentId, studentEmail, studentName, studentPassword, studentPhone)"
                            "values (?, ?, ?, ?, ?)",
                    datatuple=[studentId, studentEmail, studentName, encryptedPassword, studentPhone])
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addStudent() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        
@bp.route('/admin_delete_student', methods=['POST'])
def deleteStudent():
    try:
        requestBody = request.json
        
        studentId = requestBody['studentId']
        
        executesql(query="DELETE FROM student_table "
                            "WHERE studentId = ?",
                    datatuple=[studentId])
        
        executesql(query="DELETE FROM syndicate_members "
                            "WHERE studentId = ?",
                    datatuple=[studentId])
        
        executesql(query="DELETE FROM despatch_association_table "
                            "WHERE associationId = ?",
                    datatuple=[studentId])
        
        executesql(query="DELETE FROM message_association_table "
                            "WHERE associationId = ?",
                    datatuple=[studentId])
        
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addStudent() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})
        

@bp.route('/admin_add_student_to_course', methods=['POST'])
def addStudentToCourse():
    try:
        requestBody = request.json
        courseId = requestBody['courseId']
        studentId = requestBody['studentId']
        
        executesql(query="INSERT INTO takes_table "
                            "(courseId, studentId)"
                            "values (?, ?)",
                    datatuple=[courseId, studentId])
        return jsonify({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN addStudentToCourse() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/admin_change_password')
def adminChangePassword():
    pass

@bp.route('/admin_get_courses')
def getCourses():
    try:        
        courseData = Course.toJsonMapListFromDatabase(executesql(query="SELECT * from course_table",
                    datatuple=[]))

        teacherTakesNameList = executesql("SELECT t.teacherId, t.teacherName FROM course_table AS c INNER JOIN teacher_table AS t ON c.madeBy = t.teacherId",
                                          datatuple=[])
        
        for data in courseData:
            for i in range(0, len(teacherTakesNameList)):
                if(data['madeBy'] == teacherTakesNameList[i][0]):
                    data['madeBy'] = teacherTakesNameList[i][1]
                    break
        
        return jsonify({
                'courseList': courseData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getCourses() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})


@bp.route('/admin_get_teachers')
def getTeachers():
    try:        
        teacherData = Teacher.toJsonMapListFromDatabase(executesql(query="SELECT * from teacher_table",
                    datatuple=[]))
        
        
        return jsonify({
                'teacherList': teacherData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getTeachers() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})

@bp.route('/admin_get_students')
def getStudent():
    try:        
        studentData = Student.toJsonMapListFromDatabase(executesql(query="SELECT * from student_table",
                    datatuple=[]))
        
        
        return jsonify({
                'studentList': studentData,
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })
        
    except Exception as e:
        print("ERROR IN getStudent() method in views/admin.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR})