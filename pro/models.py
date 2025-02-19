from pro import db


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(244), unique=True, nullable=False)
	email = db.Column(db.String(244), unique=True, nullable=False)
	password = db.Column(db.String(244), nullable=False)
	roles = db.relationship('Role', secondary='User_Role' ,backref='user')
    

	def __repr__(self):
		return f"User({self.username}, {self.email}, {self.password})"



class Role(db.Model):
	role_id= db.Column(db.Integer, primary_key=True)
	role_name = db.Column(db.String(100), unique=True, nullable=False)
	users = db.relationship('User',secondary='User_Role', backref="role")
	permissions = db.relationship('Permission',secondary='Role_Permission' ,backref='role', overlaps="permissions,role")

	def __repr__(self):
		return f"Role({self.role_name})"


# for assigning a role to a user

class User_Role(db.Model):
	__tablename__='User_Role'
	user_role_id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	roleid = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)

	def __repr__(self):
		return f"User_Role{self.userid}, {self.roleid}"




class Permission(db.Model):
	perm_id = db.Column(db.Integer, primary_key=True)
	perm_name = db.Column(db.String(100), unique=True, nullable=False)
	roles = db.relationship('Role', secondary='Role_Permission' ,backref='permission', overlaps="permissions,role")

	def __repr__(self):
		return f"Permission({self.perm_name})"



# for assigning permissions to a role

class Role_Permission(db.Model):
	__tablename__='Role_Permission'
	role_permission_id = db.Column(db.Integer, primary_key=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
	perm_id = db.Column(db.Integer, db.ForeignKey('permission.perm_id'), nullable=False)

	

"""


class Group(db.Model):
	group_id = db.Column(db.Integer, primary_key=True)
	group_name = db.Column(db.String(100), nullable=False)



	def __repr__(self):
		return f"Group({self.group_name})"


class Group_User(db.Model):
	pass



class Group_Permission(db.Model):
	pass



"""

"""

class UserSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = User




user_schema = UserSchema()
users_schema = UserSchema(many=True)



class RoleSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Role




role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class PermissionSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Permission




permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)



class GroupSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Group




group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)



"""
