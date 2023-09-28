from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_login import login_user, logout_user


app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SECRET_KEY'] = 'mysecretkey'
app.app_context().push()
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from routes import *

if __name__ == '__main__':
  app.run(debug=True)
