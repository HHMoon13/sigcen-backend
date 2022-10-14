from flask import jsonify, current_app, g
import click
from app.general.constants import ServerEnum
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from app.general.util import getdbconection, executesql, generateID
import random

bp = Blueprint('db', __name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    # drop_table()
    init_db()
    insertData()
    click.echo('Initialized the database.')
    
def drop_table():
    executesql(query="DROP TABLE IF EXISTS question_table",
                    datatuple=[])
    
def insertData():
    encryptedPassword = generate_password_hash('123456')
    
    executesql(query="INSERT INTO admin_table "
                            "(adminId, adminEmail, adminName, adminPassword, adminPhone)"
                            "values (?, ?, ?, ?, ?)",
                    datatuple=['ADMIN_23476c7c_4bf0_477e_acd8_4ac22c25a6b6', 'f@a.com', 'Fawwaz', encryptedPassword, '468161'])
                        
    # studentData = [['Foysal Khan', 'f@a.com', '154313513'], ['Abdullah', 'a@a.com', '9849161'], ['Ponir', 'p@a.com', '61911361']]
    
    # for data in studentData:
    #     studentId = generateID("STUDENT")
    #     executesql(query="INSERT INTO student_table "
    #                         "(studentId, studentEmail, studentName, studentPassword, studentPhone)"
    #                         "values (?, ?, ?, ?, ?)",
    #                 datatuple=[studentId, data[1], data[0], encryptedPassword, data[2]])
        
    # teacherData = [['TEACHER_23476c7c_4bf0_477e_acd8_4ac22c25a6b6', 'Mridul', 'm@a.com', '622681'], 
    #                ['TEACHER_8f65897c_7db0_480b_ab22_58a2ac8e7736', 'Tahmid', 't@a.com', '629814'],
    #                ['TEACHER_b8894d90_73ee_4160_9299_bd43079db2b0', 'Fabiha', 'f@a.com', '7168146']]
    
    # for data in teacherData:
    #     executesql(query="INSERT INTO teacher_table "
    #                         "(teacherId, teacherEmail, teacherName, teacherPassword, teacherPhone)"
    #                         "values (?, ?, ?, ?, ?)",
    #                 datatuple=[data[0], data[2], data[1], encryptedPassword, data[3]])
          
    # teacherIdRaw = executesql("SELECT teacherId FROM teacher_table", [])
    
    # teacherId = []
    
    # for i in range(0, len(teacherIdRaw)):
    #     teacherId.append(teacherIdRaw[i][0])
    
    # courseData = [['CSE', 0], ['EEE', 1], ['GAME', 1]]
    
    # for data in courseData:
    #     courseId = generateID("COURSE")
    #     executesql(query="INSERT INTO course_table "
    #                         "(courseId, courseName, madeBy)"
    #                         "values (?, ?, ?)",
    #                 datatuple=[courseId, data[0], teacherId[data[1]]])
    
    
    
