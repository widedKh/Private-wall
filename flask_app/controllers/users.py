from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        # redirect to the route 
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['pwd'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    """
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "pwd" : pw_hash
    }
    """
    data = {
            **request.form, 'pwd':pw_hash
        }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/wall")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['pwd']):
        # if we get False after checking the password
        flash("Invalid Email/Password","login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    
    return redirect("/wall")

@app.route("/wall")
def user_show():
    if 'user_id' not in session:
        return redirect ("/")
    user_to_show = User.get_one({'id':session['user_id']})
    all_users=User.get_all({'id':session['user_id']})
    all_times=Message.get_all_messages_with_time({'id':session['user_id']})
    nb_msg_rc=Message.get_numb_of_msg_received({'id':session['user_id']})
    nb_msg_se=Message.get_numb_of_msg_sent({'id':session['user_id']})
    return render_template("wall.html",user=user_to_show,users=all_users,all_the_messages=all_times,nb_msg_rc=nb_msg_rc,nb_msg_se=nb_msg_se)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
