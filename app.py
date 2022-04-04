from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries

'''Omg whats all this ?'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Person(db.Model):
    __tablename__ = 'Person'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    notes = db.relationship('Notes', backref='author', lazy = True)

    def __repr__(self):
        return f"Person('{self.username}', '{self.email}')"

class Notes(db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key = True)
    title= db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable = False)

    def __repr__(self):
        return f"Notes('{self.title}', '{self.date_posted}')"

"""  db stuff

#Filtering in SQLAlchemy
print('*******Filtering 1*******')
for person in db.session.query(Person).filter(Person.id == 5):
    print(person.username, person.email)

#Counting in SQLAlchemy
print('*******Counting*******')
print(db.session.query(Person).filter(Person.id > 3).count())

#order by in SQLAlchemy
print('*******Order By*******')
for person in db.session.query(Person).order_by(Person.id):
    print(person.username, person.email)

# IN operator 
print('*******In Operator*******')
ids_to_select = ['1', '2', '3']
r3 = db.session.query(Person).filter(Person.id.in_(ids_to_select)).all()
for person in r3:
    print(person.username)

# AND 
print('*******AND*******')
r4 = db.session.query(Person).filter(Person.username.like('P%'), Person.id.in_([1, 10]))
for person in r4:
    print(person.username)

#raw Query
print('*******Raw Query Execution*******')
sql = text('select * from Notes')
result = db.engine.execute(sql)
for r in result:
    print(r['title'])

"""
# ROUTING FOR NAVBAR
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/course_team')
def course_team():
    return render_template('course_team.html')

@app.route('/weekly_schedule')
def weekly_schedule():
    return render_template('weekly_schedule.html')

@app.route('/lectures')
def lectures():
    return render_template('lectures.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/labs')
def labs():
    return render_template('labs.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    pagename = 'Register'
    if request.method == 'GET':
        return render_template('register.html', pagename = pagename)
    else:
        username = request.form['Username']
        email = request.form['Email']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        reg_details =(
            username,
            email,
            hashed_password
        )
        add_users(reg_details)
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('already logged in!!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        person = Person.query.filter_by(username = username).first()
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        else:
            session['name'] = username
            session.permanent = True
            return redirect(url_for('home'))

# ROUTING FOR NAVBAR

@app.route('/notes', methods = ['GET', 'POST'])
def notes():
    if request.method == 'GET':
        query_notes_result = query_notes()
        return render_template('notes.html', query_notes_result = query_notes_result)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        note_details =(
            request.form['Note_ID'],
            request.form['Title'],
            request.form['Content'],
            request.form['Your_ID']
        )
        add_notes(note_details)
        return render_template('add_success.html')

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))

""" DB STUFF

def query_notes():
    query_notes = Notes.query.all()
    return query_notes

def add_notes(note_details):
    note = Notes(id = note_details[0], title = note_details[1], content = note_details[2], person_id = note_details[3])
    db.session.add(note)
    db.session.commit()

def add_users(reg_details):
    person = Person(username = reg_details[0], email = reg_details[1], password = reg_details[2])
    db.session.add(person)
    db.session.commit()

"""

if __name__ == '__main__':
    app.run(debug=True)
