from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries
#rom sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

hush_hush = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
#ripped off of flask's site for an example of a good secret key

# https://piazza.com/class/kxj5alixpjg4ft?cid=289 for info on these sets
students = set()
instructors = set()

app = Flask(__name__)
app.config['SECRET_KEY'] = hush_hush
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ass3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 2)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ass3.db'
#engine = create_engine('sqlite:///ass3.db')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#base = declarative_base()
"""
class Person(base):
    __tablename__ = 'Person'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    notes = db.relationship('Notes', backref='author', lazy = True)

    #def __repr__(self):
        #return f"Person('{self.username}', '{self.email}')"

class Notes(base):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    title= db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable = False)

<<<<<<< Updated upstream
    def __repr__(self):
        return f"Notes('{self.title}', '{self.date_posted}')"
=======
    #def __repr__(self):
        #return f"Notes('{self.title}', '{self.date_posted}')"
"""


class Account(db.Model):
    __tablename__ = 'Account'
    Account_id = db.Column(db.Integer, primary_key = True, unique = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Account('{self.username}', '{self.email}, {self.password}, {self.type}')"

class Student(db.Model):
    __tablename__ = 'Student'
    username = db.Column(db.String(20), unique=True, nullable = False) 
    Student_id = db.Column(db.Integer, db.ForeignKey('Account.Account_id'), nullable = False, primary_key = True)

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    username = db.Column(db.String(20), unique=True, nullable = False) 
    Instructor_id = db.Column(db.Integer, db.ForeignKey('Account.Account_id'), nullable = False, primary_key = True)

class Marks(db.Model):
    __tablename__ = 'Marks'
    student_id = db.Column(db.Integer, db.ForeignKey('Student.Student_id'), nullable = False, primary_key = True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.Instructor_id'), nullable = False)
    accessment = db.Column(db.String(20), nullable = False, primary_key = True)
    grade = db.Column(db.Integer, nullable = False)

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    q1 = db.Column(db.Integer, nullable = False)
    q2 = db.Column(db.Integer, nullable = False)
    q3 = db.Column(db.Integer, nullable = False)
    q4 = db.Column(db.Integer, nullable = False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.Instructor_id'), nullable = False)
    Feed_id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)

class Remark(db.Model):
    __tablename__ = 'Remark'
    accessment = db.Column(db.String(20),db.ForeignKey('Marks.accessment'), nullable = False, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.Student_id'), nullable = False, primary_key = True)
    blurb = db.Column(db.String(100), unique = False, nullable = False)

##base.metadata.create_all(engine)
"""
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

#new pages for A3
@app.route('/stu_home')
def stu_home():
    return render_template('stu_home.html')

@app.route('/submit_feedback')
def submit_feedback():
    return render_template('submit_feedback.html')

@app.route('/instr_home')
def instr_home():
    return render_template('instr_home.html')    

@app.route('/view_feedback')
def view_feedback():
    return render_template('view_feedback.html')

@app.route('/view_remark')
def view_remark():
    return render_template('view_remark.html') 

@app.route('/enter_marks')
def enter_marks():
    return render_template('enter_marks.html') 

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    pagename = 'Register'
    if request.method == 'GET':
        return render_template('register.html', pagename = pagename)
    else:
        username = request.form['Username']
        email = request.form['Email']
        
        #add registered users to the correct set

        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        types= request.form['Acc_Type'] 
        reg_details =(
            username,
            email,
            hashed_password,
            types
        )
        if ((types == 'Student') == True):
            students.add(username)
        else:
            instructors.add(username)
        
        add_users(reg_details)
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('already logged in!!')

            #which page should be shown?
            if ('name' in students):
                return redirect(url_for('stu_home'))
            elif ('name' in instructors):
                return redirect(url_for('instr_home'))
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')
    else: #this means POST
        username = request.form['Username']
        password = request.form['Password']
        account = Account.query.filter_by(username = username).first()
        #if user fails authentication
        if not account or not bcrypt.check_password_hash(account.password, password):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        #if user is recognised
        else:
            session['name'] = username
            if (account.type == Student ):
                session.permanent = True
                return redirect(url_for('stu_home.html'))
            elif (account.type == Instructor ):
                session.permanent = True
                return redirect(url_for('instr_home.html'))
            else:
                flash('Please check your login details and try again', 'error')
                return render_template('login.html') 

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

"""
def query_notes():
    query_notes = Notes.query.all()
    return query_notes

def add_notes(note_details):
    note = Notes(id = note_details[0], title = note_details[1], content = note_details[2], person_id = note_details[3])
    db.session.add(note)
    db.session.commit()
"""

def add_users(reg_details):
    account = Account(username = reg_details[0], email = reg_details[1], password = reg_details[2], type = reg_details[3])
    db.session.add(account)
    db.session.commit()




if __name__ == '__main__':
    app.run(debug=True)



