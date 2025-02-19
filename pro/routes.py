from pro import app, db

from flask import request, session, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from pro.models import User, Role, Permission





@app.route('/register', methods=['POST']).
def regsiter():
	if request.method == 'POST':
		data = request.get_json()
		if data['password1'] == data['password2']:
			hashed_password = generate_password_hash(data['password1'])
			user = User(username=username, email=email, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			return jsonify({"user": user})
		else:
			return 'Register'


@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		data = request.get_json()
		username = data["username"]
		password = data["password"]

		user = User.query.filter_by(username=username).first()

		if check_password_hash(user.password, password):
			session['user'] = user.username
			session['user_id'] = user.user_id
			return jsonify({'message': 'You are Logged In'})
		else:
			return jsonify({'message': 'Check Your Password'})

	return jsonify({'message': 'Please Log In'})






@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user', None)
		return jsonify({"message": "You Are Logged Out"})
	else:
		return jsonify({"message": "Please Log In"})





@app.route('/users', methods=["POST"])
def add_user():
	if 'user' in session:

		if request.method == 'POST':
			data = request.get_json()
			username = data["username"]
			email = data["email"]
			password = data["password"]
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			return jsonify({'message': 'Added A User'})
	else:
		return jsonify({'message': 'Add A user'})




@app.route('/users', methods=['GET'])
def get_users():
	if 'user' in session:

		users = User.query.all()

		return jsonify({"users": user})

	else:
		return jsonify({"message": "No users found"})



@app.route('/users/<int:user_id>', methods=['GET'])
def getuser(user_id):
	if 'user' in session:

		user = User.query.filter_by(user_id=user_id).first()
		return jsonify({"user": user})

	else:
		return jsonify({"message": "Please Log In"})



@app.route('/users/<int:user_id>/update', methods=["POST"])
def update_user(user_id):
	if 'user' in session:
		user = User.query.filter_by(user_id=user_id).first()
         
		if request.method == 'POST':
			data = request.get_json()
			user.username = data['username']
			user.email = data['email']
			user.password = data['password']
			db.session.commit()
			return jsonify({"user": user})

		

		return jsonify({"message": "Update a user"})

	else:
		return jsonify({"message": "Please Log In"})


@app.route("/users/<int:user_id>/delete", methods=['DELETE'])
def delete_user(user_id):
	if 'user' in session:
		user = User.query.filter_by(user_id=user_id).delete()
		db.session.commit()
		return jsonify({"message": "User Deleted"})

	else:
		return jsonify({"message": "Please Log In"})



@app.route('/roles')
def get_roles():
	if 'user' in session:
		roles = Role.query.all()
		return jsonify({"roles": roles})
	else:
		return jsonify({"message": "Please Log In"})


@app.route('/roles', methods=['POST'])
def add_role():
	if 'user' in session:
		if request.method == ['POST']:
			data = request.get_json()
			role = Role(role_name=data['role_name'])
			return jsonify({"role": role})

	else:
		return jsonify({"message": "Please Log In"})



@app.route('/roles/<int:role_id>')
def get_role(role_id):
	if 'user' in session:
		role = Role.query.filter_by(role_id=role_id).first()
		return jsonify({"role": role})

	else:
		return jsonify({"message": "Please Log In"})


@app.route('/roles/<int:role_id>/update', methods=['GET', 'POST'])
def update_role(role_id):
	if 'user' in session:
		role = Role.query.filter_by(role_id=role_id).first()
		data = request.get_json()
		role.role_name = data['role_name']
		db.session.commit()
		return jsonify({"role": role})

	else:
		return jsonify({"message": "Please Log In"})





@app.route('/roles/<int:role_id>/delete')
def delete_role(role_id):
	if 'user' in session:
		role = Role.query.filter_by(role_id=role_id).first()
		db.session.delete(role)
		db.session.commit()

	else:
		return jsonify({"message": "Please Log In"})




@app.route('/roles/<int:role_id>/assign', methods=['POST'])
def assign_role(role_id, user_id):
	if 'user' in session:
		if request.method == 'POST':
			user = User.query.filter_by(user_id=user_id).first()
			role = Role.query.filter_by(role_id=role_id).first()
			assign_role = User_Role(userid=user_id, roleid=role_id)
			db.session.add(assign_role)
			db.session.commit()
			return jsonify({"assign_role": assign_role})
	else:
		return jsonify({"message": "Please Log In"})


@app.route('/roles/<int:role_id>/unassign/change_role', methods=['PUT'])
def unassign_role(role_id, user_id):
	if 'user' in session:
		if request.method == 'PUT':
			user_role = User_Role.query.filter_by(userid=user_id, roleid=role_id).first()
			data = request.get_json()
			user_role.userid = data['user_id']
			return jsonify({"user_role": user_role})
	else:
		return jsonify({"message": "Please Log In"})




