"""
Models configuration file that contains all Models and ENUMs
"""
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from flask_security import RoleMixin, AsaList
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY
from flask_security import RoleMixin
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
    return str(uuid4())


class Permission(Enum):
    """
    Role Permissions defination
    """
    CREATE = 'Create'
    READ = 'Read'
    UPDATE = 'Update'
    DELETE = 'Delete'
    ADMIN = 'Admin'


# 
# Gender Enum Model
# This is the Gender Enum Model and its variable to be created in the database
#
class Gender(Enum):
    """
    Gender Enum defination
    """
    MALE = "Male"
    FEMALE = "Female"


class Permission(db.Model):
    """
    Permission Model defination
    """
    __tablename__ = "permissions"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(20), nullable=False, unique=True)
    # Relationships
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')



# 
# Role Model
# This is the Role Model and its variable to be created in the database
#
class Role(RoleMixin, db.Model):
    """
    Role Model defination
    """
    __tablename__ = "roles"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')
    users = db.relationship('User', secondary='user_roles', back_populates='roles')

    # Initialization of roles 
    def __init__(self, name, description=None, permissions=None):
        self.name = name
        self.description = description
        self.permissions = permissions or []
    
    # Add role permission method
    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

    # Remove role permission method
    def remove_permission(self, permission):
        if permission in self.permissions:
            self.permissions.remove(permission)

    # Reset role permission method
    def reset_permissions(self):
        self.permissions = []

    # Checks for role permission
    def has_permission(self, permission):
        return permission in self.permissions


class RolePermission(db.Model):
    """
    Role Permissions Model defination
    """
    __tablename__ = "role_permissions"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id', name='fk_role_id', ondelete='CASCADE'))
    permission_id = db.Column(db.String(36), db.ForeignKey('permissions.id', name='fk_permission_id', ondelete='CASCADE'))


class UserStatus(Enum):
    """
    User Status Enum defination
    """
    ACTIVE = 'Active'       # User is active and has access to the system
    INACTIVE = 'Inactive'   # User is inactive and cannot access the system
    SUSPENDED = 'Suspended' # User account is temporarily disabled
    PENDING = 'Pending'     # User account is awaiting approval or activation
    BANNED = 'Banned' 
# 
# User Model
# This is the User Model and its variable to be created in the database
#
class User(UserMixin, db.Model):
    """
    User Model defination
    """
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    last_login = db.Column(db.DateTime, nullable=True)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    voters = db.relationship('Voter', backref='user', lazy=True)


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
    User_Roles Model defination 
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
    County Model defination
    """
    __tablename__ = "counties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    constituencys = db.relationship('Constituency', backref='county', lazy=True)



# 
# Constituency Model
# This is the Constituency Model and its variable to be created in the database
#
class Constituency(db.Model):
    """
    Constituency Model defination
    """
    __tablename__ = "constituencies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id', name='fk_county_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    voters = db.relationship('Voter', backref='constituency', lazy=True)



# 
# Voter Model
# This is the Voter Model and its variable to be created in the database
#
class Voter(db.Model):
    """
    Voter Model defination
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
    date_registered = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    motionvotes = db.relationship('MotionVote', backref='voter', lazy=True)
    agendavote = db.relationship('AgendaVote', backref='voter', lazy=True)


class Category(db.Model):
    """
    Motion Category Model defination
    """
    __tablename__="categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    motions = db.relationship('Motion', backref='category', lazy=True)

class FinalVote(Enum):
    """
    Final Vote Enum defination
    """
    SUPPORT = "Support"
    DONT_SUPPORT = "Don't Support"
    OTHER = "Other"
    TIE = "Tie"
    NO_VOTES = "No votes yet"

class MotionStatus(Enum):
    """
    Motion Status Enum defination
    """
    DRAFT = 'Draft'
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    ARCHIVED = 'Archived'

class Motion(db.Model):
    """
    Motion Model defination
    """
    __tablename__ = "motion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', name='fk_category_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    final_vote = db.Column(db.Enum(FinalVote), nullable=False, default=FinalVote.NO_VOTES)
    status = db.Column(db.Enum(MotionStatus), nullable=False, default=MotionStatus.DRAFT)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    motionvotes = db.relationship('MotionVote', backref='motion', lazy=True)
    agendas = db.relationship('Agenda', backref='motion', lazy=True)


class SupportOptions(Enum):
    """
    Motion Support Enum defination
    """
    ISUPPORT = 'I support'
    IDONOTSUPPORT = 'I do not Support'
    OTHERS = 'Others'


class MotionVote(db.Model):
    """
    Motion Vote Model defination
    """
    __tablename__ = "MotionVote"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voter_id = db.Column(db.String(36), db.ForeignKey('voters.id', name='fk_voter_id'), nullable=False)
    motion_id = db.Column(db.Integer, db.ForeignKey('motion.id', name='fk_motion_id'), nullable=False)
    vote = db.Column(db.Enum(SupportOptions), nullable=False)
    other_text = db.Column(db.String(100), nullable=True)
    voted_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())



class Agenda(db.Model):
    """
    Agenda Model defination
    """
    __tablename__ = "agenda"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    motion_id = db.Column(db.Integer, db.ForeignKey('motion.id', name='fk_motion_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # Relationships
    agendavotes = db.relationship('AgendaVote', backref='agenda', lazy=True)



class AgendaVote(db.Model):
    """
    Agenda Vote Model defination
    """
    __tablename__ = "agenda_vote"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voter_id = db.Column(db.String(36), db.ForeignKey('voters.id', name='fk_voter_id'), nullable=False)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id', name='fk_agenda_id'), nullable=False)
    vote = db.Column(db.Boolean, nullable=False, default=True)
    voted_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())