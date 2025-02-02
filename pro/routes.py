from pro import app, db

from flask import render_template, request, redirect, url_for, session, flash

from werkzeug.security import generate_password_hash, check_password_hash

from pro.models import User

"""
def current_user(user_id):
	if 'user':
		user = session['user']
	    user = User.query.filter_by(user_id=user_id)
	else:
		flash("You nedd to login")
		retur redirect(url_for("login"))

"""

@app.route('/')
def home():
	return render_template('home.html') 




@app.route('/register', methods=['GET', 'POST'])
def regsiter():
	if request.method == 'POST':
		username = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		confirm_password = request.form["confirm_password"]
		if password == confirm_password:
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for("login"))

	return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]

		user = User.query.filter_by(username=username).first()

		if check_password_hash(user.password, password):
			session['user'] = user.username
			session['user_id'] = user.user_id
			return redirect(url_for("dashboard"))

	return render_template("login.html")



@app.route('/dashboard')
def dashboard():
	if 'user' in session:
		user = session['user']
		flash(f"Hello {user}")
	return render_template("dashboard.html")


@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user', None)
		return redirect(url_for("login"))
	else:
		return redirect(url_for("login"))



@app.route('/profile')
def profile():
	if 'user' in session:
		user = session['user']
		user.form["username"] = user.username 
		user.form["email"] = user.email 
	return render_template("profile.html")



@app.route('/user', methods=["GET", "POST"])
def adduser():
	if 'user' in session:

		if request.method == 'POST':
			username = request.form.get("username")
			email = request.form.get("email")
			password = request.form.get("password")
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('getusers'))
		return render_template("adduser.html")

	else:
		return redirect(url_for("login"))



@app.route('/getusers')
def getusers():
	if 'user' in session:

		users = User.query.all()

		return render_template("getallusers.html", users=users)

	else:
		return redirect(url_for("login"))

@app.route('/getuser/<int:user_id>')
def getuser(user_id):
	if 'user' in session:

		user = User.query.filter_by(user_id=user_id).first()
		return render_template("userinfo.html", user=user)

	else:
		return redirect(url_for("login"))



@app.route('/updateuser/<int:user_id>', methods=["GET", "POST"])
def updateuser(user_id):
	if 'user' in session:
		user = User.query.filter_by(user_id=user_id).first()
         
		if request.method == 'POST':
			
			user.username = request.form.get("username")
			user.email = request.form.get("email")
			user.password = request.form.get("password")
			db.session.commit()
			return redirect(url_for("getuser", user_id=user.user_id))

		

		return render_template("updateuser.html", user=user)

	else:
		return redirect(url_for("login"))


@app.route("/deleteuser/<int:user_id>")
def deleteuser(user_id):
	if 'user' in session:

		user = User.query.filter_by(user_id=user_id).delete()
		db.session.commit()
		return redirect(url_for("getusers"))

	else:
		return redirect(url_for("login"))
