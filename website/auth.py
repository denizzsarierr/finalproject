from flask import Blueprint,render_template,request,flash,redirect,url_for
from . import models,db
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from flask_login import login_user,login_required,logout_user,current_user  

auth = Blueprint("auth",__name__)


@auth.route('/login',methods = ["GET","POST"])
def login():

    form = request.form

    if request.method == "POST":

        username = form.get("username")
        password = form.get("password1")

        user = User.query.filter_by(username = username).first()

        if user:

            if check_password_hash(user.password,password):
                
                flash("Logged in.",category="success")
                login_user(user,remember=True)
                #Remember user is logged in until log out. Even if the site closed.
                return redirect(url_for('views.home'))
            else:
                flash("Error",category='danger')
        else:

            flash("User does not exist",category='error')



    return render_template('login.html',user = current_user)

@auth.route('/logout',methods = ["GET","POST"])
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods = ["GET","POST"])
def sign_up():

    form = request.form
    
    if request.method == "POST":
        email = form.get("email")
        username = form.get("username")
        password1 = form.get("password1")
        password2 = form.get("password2")

        if len(email) > 0 and len(username) > 0 and len(password1) > 0 and len(password2) > 0:
            new_user = models.User(email=email,username=username,password = generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created",category="success")
            return redirect(url_for('views.home'))





    return render_template('signup.html',user = current_user)