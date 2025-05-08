from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from helpers.config_img import UPLOAD_PATH
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('database/config.py')
app.config['UPLOAD_PATH'] = UPLOAD_PATH

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views.views_movies import *
from views.views_user import *
    

if __name__ == '__main__':
    app.run(debug=True) 
