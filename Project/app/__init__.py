from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Use SECRET_KEY from .env
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    
    print(f"Database path: {database_path}")


    db.init_app(app)

    with app.app_context():
        try:
            from .models import User, Place, Review
            print("Creating tables...")
            db.create_all()
            print("Tables created.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    from .routes import main
    app.register_blueprint(main)

    return app
