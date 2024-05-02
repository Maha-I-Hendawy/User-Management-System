from pro import app, db

from flask import render_template, request, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash

from pro.models import User





@app.route('/')
def home():
	return render_template('home.html') 



@app.route('/user', methods=["GET", "POST"])
def adduser():
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



@app.route('/getusers')
def getusers():
	users = User.query.all()

	return render_template("getallusers.html", users=users)



@app.route('/getuser/<int:id>')
def getuser(id):
	user = User.query.filter_by(id=id).first()
	return render_template("userinfo.html", user=user)



@app.route('/updateuser/<int:id>', methods=["GET", "POST"])
def updateuser(id):
	if request.method == 'POST':
		user = User.query.filter_by(id=id).first()
		user.username = request.form.get("username")
		user.email = request.form.get("email")
		user.password = request.form.get("password")
		db.session.commit()
		return redirect(url_for("getuser", id=id))

	

	return render_template("updateuser.html")


@app.route("/deleteuser/<int:id>")
def deleteuser(id):
	user = User.query.filter_by(id=id).delete()
	db.session.commit()
	return redirect(url_for("getusers"))
