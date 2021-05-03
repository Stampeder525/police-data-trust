"""Define the SQL classes for Users."""
from flask_sqlalchemy import SQLAlchemy
from flask_serialize.flask_serialize import FlaskSerialize
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_user import current_user, login_required, roles_required, UserManager, SQLAlchemyAdapter
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from backend.database.core import db

import enum

fs_mixin = FlaskSerialize(db)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


# Define the User data-model.
class Users(db.Model, UserMixin):
    """The SQL dataclass for an Incident."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    # @property
    # def password(self):
    #     raise AttributeError("Password is not a readable attribute")

    def verify_password(self, pw):
        return check_password_hash(self.password, pw)


db_adapter = SQLAlchemyAdapter(db, Users)
user_manager = UserManager(db_adapter)

 # Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))