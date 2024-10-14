"""
Models configuration file that contains all Models and ENUMs
"""
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import RoleMixin, UserMixin, AsaList
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.mutable import MutableList
from enum import Enum
from datetime import datetime
from .extensions import db
# from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# configs
# database linked with sqlalchemy
# db = SQLAlchemy()



# Model Definations Starts Here

# Function to generate UUIDs
def generate_uuid():
    """
    A function to generate UUIDs
    """
    return str(uuid.uuid4())


# 
# Gender Enum Model
# This is the Gender Enum Model and its variable to be created in the database
#
class Gender(Enum):
    """
    Gender Enum Defination
    """
    MALE = "Male"
    FEMALE = "Female"



# 
# Role Model
# This is the Role Model and its variable to be created in the database
#
class Role(RoleMixin, db.Model):
    """
    Role Model Defination
    """
    __tablename__ = "roles"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True))
    # Relationships
    users = db.relationship('User', secondary='user_roles', back_populates='roles')



# 
# User Model
# This is the User Model and its variable to be created in the database
#
class User(UserMixin, db.Model):
    """
    User Model Defination
    """
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    members = db.relationship('Member', backref='user', lazy=True)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



# 
# User Roles Model
# This is a User to Role Many-To-Many relationship Table
#
class UserRole(db.Model):
    """
    User_Roles Model Defination 
    """
    __tablename__ = "user_roles"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', name='fk_user_id', ondelete='CASCADE'))
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id', name='fk_role_id', ondelete='CASCADE'))



# 
# County Model
# This is the County Model and its variable to be created in the database
#
class County(db.Model):
    """
    County Model Defination
    """
    __tablename__ = "counties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    # Relationships
    constituencys = db.relationship('Constituency', backref='county', lazy=True)



# 
# Constituency Model
# This is the Constituency Model and its variable to be created in the database
#
class Constituency(db.Model):
    """
    Constituency Model Defination
    """
    __tablename__ = "constituencies"
    id = db.Column(db.Integer, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id', name='fk_county_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    # Relationships
    voters = db.relationship('Voter', backref='constituency', lazy=True)



# 
# Voter Model
# This is the Voter Model and its variable to be created in the database
#
class Voter(db.Model):
    """
    Voter Model Defination
    """
    __tablename__ = "voters"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', name='fk_user_id'), nullable=False)
    constituency_id = db.Column(db.Integer, db.ForeignKey('constituencies.id', name='fk_constituency_id'), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    othername = db.Column(db.String(20), nullable=True)
    fullname = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=False)
    id_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=True)
    voted = db.Column(db.Boolean, nullable=False, default=False)
    has_read = db.Column(db.Boolean, nullable=False, default=False)
    date_registered = db.Column(db.DateTime, nullable=False)
    # Relationships
    



class Question(db.Model):
    """
    Question Model Defination
    """
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    # Relationships
    options = db.relationship('Option', backref='question', lazy=True)



class Option(db.Model):
    """
    Option Model Defination
    """
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', name='fk_question_id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    # Relationships
    results = db.relationship('Result', backref='option', lazy=True)



class Result(db.Model):
    """
    Result Model Defination
    """
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id', name='fk_option_id'), nullable=False)
    no_support_score = db.Column(db.Integer, nullable=False)
    others_score = db.Column(db.Integer, nullable=False)
    last_sync_date = db.Column(db.DateTime, nullable=True)