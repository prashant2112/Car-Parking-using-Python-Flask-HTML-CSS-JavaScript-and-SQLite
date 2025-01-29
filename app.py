from flask import Flask,render_template, request, redirect, url_for, session,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///carparking.db"
app.config['SECRET_KEY'] = 'project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ="project"
db = SQLAlchemy(app)
app.app_context().push()






class carparking(db.Model):
    sno=db.Column(db.Integer, primary_key = True)
    NAME=db.Column(db.String(100), nullable= False)
    CAR_NUMBER=db.Column(db.String(100), nullable= False)
    DATE=db.Column(db.DateTime, default= datetime.utcnow)
     

    def __repr__(self) -> str:
        return f"{self.sno} - {self.NAME}"

class user(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(100), unique=True ,nullable= False)
    password = db.Column(db.String(30), nullable= False)

class CAR(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    NAME=db.Column(db.String(100), nullable= False)
    CAR_NUMBER=db.Column(db.String(100), nullable= False)

    


   
    
    
@app.route('/')
def main():
    return render_template('main.html')
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/instant_parking',methods=['GET','POST'])
def instant_parking():
    if request.method=='POST':
        name=(request.form['name'])
        car_no = (request.form['carno'])
        display= carparking(NAME= name, CAR_NUMBER=car_no)
        db.session.add(display)
        db.session.commit()

        parkingno=2


        session["parkingno"]= parkingno
        return redirect(url_for("dashboard"))
    else:
        return render_template('instant_parking.html')
    
# car parking algorithm
@app.route('/dashboard')
def dashboard():
    if "parkingno" in session:
        parkingno=session["parkingno"]
        parkingno=parkingno
        return render_template('dashboard.html', parkingno=parkingno)
    else:
        return redirect(url_for("login"))
        



@app.route('/admin')
def admin():
    display= carparking.query.all()
    
    print(display)
    
    Users=user.query.all()
    print(Users)
    return render_template('admin.html',display=display, Users=Users)


@app.route('/delete/<int:sno>')
def delete(sno):
    display= carparking.query.filter_by(sno=sno).first()
    db.session.delete(display)
    db.session.commit()
    return redirect("/admin")

@app.route('/update/<int:sno>', methods=['GET',"POST"])
def update(sno):
    if request.method=='POST':
        name=(request.form['name'])
        car_no = (request.form['carno'])
        display = carparking.query.filter_by(sno=sno).first()
        display.NAME= name
        display.CAR_NUMBER= car_no
        db.session.add(display)
        db.session.commit()
        return redirect("/admin") 
    display = carparking.query.filter_by(sno=sno).first()
    return render_template('update.html', display=display)

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method=='POST':
        Username = request.form['Username']
        password = request.form['password']

        if not (Username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            Username = Username.strip()
            password = password.strip()

        Users = user.query.filter_by(Username=Username).first()

        if Users.password == password:
            session[Username] = True
            return redirect(url_for("instant_parking"))
        else:
            return redirect(url_for("login"))
    
    return render_template('login.html')

@app.route('/register', methods =['GET','POST'])
def register():
    if request.method=='POST':
        Username = request.form['Username']
        password = request.form['password']
        
        Users=user(Username=Username,password=password)
        Users.Username = Username
        Users.password = password
        db.session.add(Users)
        db.session.commit()
        return redirect('/login')
    

    return render_template('register.html')



        
    
    
    
    
    
    return render_template('dashboard.html', parkingno=parkingno)



@app.route('/payment')
def payment():
    return render_template('main.html')
@app.route('/active')
def activity():
    return render_template('active.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)
