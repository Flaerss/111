from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def init_app(app):
    """Инициализация расширения SQLAlchemy для Flask"""
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()