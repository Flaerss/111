from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return 'Приложение работает'

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
