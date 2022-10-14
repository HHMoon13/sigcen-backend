import logging
import os
from flask import Flask
from app.database import init_app, get_db
import app.views.admin as admin_view
import app.views.user as user_view
import app.views.student as student_view
import app.views.teacher as teacher_view
from flask_cors import CORS
import app

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'pass'
    # app.config['MYSQL_DB'] = 'flask'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    
    init_app(app)
    
    app.register_blueprint(admin_view.bp)
    app.register_blueprint(database.bp)
    app.register_blueprint(user_view.bp)
    app.register_blueprint(student_view.bp)
    app.register_blueprint(teacher_view.bp)
    
    # init_db_command()

    return app
