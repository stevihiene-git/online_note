# __init__.py (updated)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Initialize Migrate

def create_app():
    
    # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Configure instance path for Vercel
    instance_path = None
    if os.environ.get('VERCEL'):
        # On Vercel, use /tmp for instance directory
        instance_path = '/tmp/instance'
    
    app = Flask(__name__, 
                template_folder=os.path.join(BASE_DIR, 'templates'),  # Correct path
                static_folder=os.path.join(BASE_DIR, 'static'))      



        # Configuration
    
    app.config['SECRET_KEY'] = '2d2c5c6476929240e999d4487136ecf06f223dc9e7c381272bf7ae4eaf0c13ab'  # to be Changed in production!
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_cgBmFfx74CHD@ep-holy-dew-ad13mo4d-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notedb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
            # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)  # Initialize migrate with app and db
    login_manager.login_message_category = 'info'
    
    from note_app.models import User, Note
    
    # Import models within app context to avoid circular imports
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from note_app.views import views2
    from note_app.auth import auth2
    
    app.register_blueprint(views2, url_prefix='/')
    app.register_blueprint(auth2, url_prefix='/')
    

    
    return app


  
