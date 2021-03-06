from flask import Flask, render_template, url_for
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from youtube import printWAV
import time, random, threading
from turbo_flask import Turbo
from flask_bcrypt import Bcrypt
from sqlalchemy import exc




app = Flask(__name__)
app.config['SECRET_KEY'] = 'd7c2cac4b6e388eaf69012b25c3fd6f8'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

interval=10
FILE_NAME = "TaylorSwift.wav"
turbo = Turbo(app)
bcrypt = Bcrypt(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=False, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/new")
def new():
    return render_template('new.html', subtitle='Second Page', text = 'This is our second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
      encrypted = bcrypt.generate_password_hash(form.password.data)
      #print(encrypted)
      if bcrypt.check_password_hash(encrypted, form.password.data):
        user = User(username=form.username.data, email=form.email.data, password=encrypted)
        db.session.add(user)
        try:
          db.session.commit()
        except (exc.IntegrityError, exc.OperationalError):
          print("Username already in use.")
        else:
          flash(f'Account created for {form.username.data}!', 'success')
          return redirect(url_for('home')) # if so - send to home page
    
    return render_template('register.html', title='Register', form=form)

@app.route("/captions")
def captions():
    TITLE = "You belong with me"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)
  
@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()

    #starting thread that will time updates
    threading.Thread(target=update_captions).start()

@app.context_processor
def inject_load():
    # getting previous time stamp
    file = open("pos.txt","r")
    pos = int(file.read())
    file.close()

    # writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()

    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}

def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
