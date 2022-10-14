from flask_bcrypt import generate_password_hash, check_password_hash
from app.general.util import getdbconection, executesql, decodeJson
from app.general.constants import ServerEnum
from flask import jsonify, current_app, g
import click
import app.views.admin as admin_view
import app.views.student as student_view
import app.views.teacher as teacher_view
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('user', __name__)

@bp.route('/login', methods = ['POST'])
def login():
    try:
        userData = request.json
        userEmail = userData['userEmail']
        userPassword = userData['userPassword']
        userType = userData['userType']

                
        if userType == 'ADMIN':
            return admin_view.loginAdmin(userEmail, userPassword)
        
        elif userType == 'TEACHER':
            return teacher_view.loginTeacher(userEmail, userPassword)
        
        elif userType == 'STUDENT':
            return student_view.loginStudent(userEmail, userPassword)
        
    except Exception as e:
        print("ERROR IN login() method in views/user.py")
        print(e)
        return jsonify({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })