# __init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Get the base directory
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Configure for Vercel production
    app = Flask(__name__,
                instance_path='/tmp',
                instance_relative_config=True,
                template_folder=os.path.join(BASE_DIR, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static'))

    # # Use Neon PostgreSQL from environment variable
    # database_url = os.environ.get('DATABASE_URL')
    
    # # Check if DATABASE_URL is set; if not, an error will occur
    # if not database_url:
    #     # This will cause the application to fail to start, which is the desired behavior
    #     # in a production environment if a critical variable is missing.
    #     raise RuntimeError("DATABASE_URL environment variable is not set. Please configure it in your Vercel project settings.")

    # Fix for Neon's postgres:// prefix
    # if database_url.startswith('postgres://'):
    #     database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_cgBmFfx74CHD@ep-holy-dew-ad13mo4d-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuration - use environment variables for security
    app.config['SECRET_KEY'] = '2d2c5c6476929240e999d4487136ecf06f223dc9e7c381272bf7ae4eaf0c13ab'
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Create database tables
    with app.app_context():
        from note_app import models
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database error: {e}")
    
    # Register blueprints
    from note_app.views import views2
    from note_app.auth import auth2
    
    app.register_blueprint(views2, url_prefix='/')
    app.register_blueprint(auth2, url_prefix='/')
    
    return app

