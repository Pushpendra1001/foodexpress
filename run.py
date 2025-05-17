from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(level=logging.INFO)


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')


app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 30,  
    'max_overflow': 30,  
    'pool_recycle': 1800,  
    'pool_pre_ping': True,  
    'pool_timeout': 60,  
}


db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    with app.app_context():
        
        from views import *
        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        
        
        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('error.html', error=404), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            db.session.rollback()
            return render_template('error.html', error=500), 500
            
        db.create_all()
    app.run(debug=True)