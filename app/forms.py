"""Forms defination file."""
from models import *
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField, BooleanField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

#----------------------------------------------------------------------------------------#
# Form defination Start Here

#========================================================================================#
# Auth View Forms Starts Here
#----------------------------------------------------------------------------------------#

#========================================================================================#
# Login Form
#========================================================================================#
class LoginForm(FlaskForm):
    """User Login form defination"""
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Register User Form
#========================================================================================#
class RegisterForm(FlaskForm):
    """User Registration form defination"""
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"First Name", "class":"form-control", "required":"required"})
    lastname = StringField("Last Name", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"Last Name", "class":"form-control", "required":"required"})
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
    roles = SelectField("Roles", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Roles", "class":"form-control form-select"})
    active = BooleanField("Active User?", render_kw={"placeholder":"Active?", "type":"checkbox", "class":"form-check-input"})
#========================================================================================#

#----------------------------------------------------------------------------------------#
# Auth View Forms Ends Here
#========================================================================================#





#========================================================================================#
# Settings View Forms Starts Here
#----------------------------------------------------------------------------------------#

#========================================================================================#
# Role Form
#========================================================================================#
class RoleForm(FlaskForm):
    """Role form defination"""
    name = StringField("Role", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"Role", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# User Form
#========================================================================================#
class UserForm(FlaskForm):
    """User Registration form defination"""
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"First Name", "class":"form-control", "required":"required"})
    lastname = StringField("Last Name", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Last Name", "class":"form-control", "required":"required"})
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Phone Number", "type":"tel", "class":"form-control", "required":"required"})
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
    roles = SelectField("Roles", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Roles", "class":"form-control form-select"})
    active = BooleanField("Active User?", render_kw={"placeholder":"Active?", "type":"checkbox", "class":"form-check-input"})
#========================================================================================#


#========================================================================================#
# Image Upload Form
#========================================================================================#
class ImageForm(FlaskForm):
    """Image Upload form defination"""
    photo_name = FileField("Image", validators=[FileAllowed(['png', 'jpg'], 'Image only!')])
#========================================================================================#


#========================================================================================#
# Goups Form
#========================================================================================#
class GroupForm(FlaskForm):
    """Group form defination"""
    name = StringField("Group Name", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder":"Group Name", "class":"form-control", "required":"required"})
    contact_person = StringField("Contact Person", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder":"Contact Person", "class":"form-control", "required":"required"})
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Phone Number", "type":"tel", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Loan Type Form
#========================================================================================#
class LoanTypeForm(FlaskForm):
    """Loan Type form defination"""
    name = StringField("Loan Type", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Loan Type", "type":"text", "class": "form-control", "required":"required"})
#========================================================================================#

#----------------------------------------------------------------------------------------#
# Settings View Forms Ends Here
#========================================================================================#



#========================================================================================#
# Admin View Forms Starts Here
#----------------------------------------------------------------------------------------#
#========================================================================================#
# Member Forms
#========================================================================================#
class MemberForm(FlaskForm):
    """Member form defination"""
    member_number = StringField("Member Number e.g OC2024/1", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Member Number", "type":"text", "class": "form-control", "required":"required"})
    form_number = StringField("Form Number e.g FN2024/1", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Form Number", "type":"text", "class": "form-control", "required":"required"})
    group_id = SelectField("Group", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Group", "class":"form-control form-select", "required":"required"})
    surname = StringField("Surname", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Surname", "type":"text", "class": "form-control", "required":"required"})
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "First Name", "type":"text", "class": "form-control", "required":"required"})
    othername = StringField("Other Names", validators=[Length(max=20)],
                       render_kw={"placeholder": "Second Name", "type":"text", "class": "form-control"})
    gender = SelectField("Gender", choices=[(gender.name, gender.value) for gender in Gender],
                        render_kw={"placeholder":"Gender", "class":"form-control form-select", "required":"required"})
    marital_status = SelectField("Marital Status", choices=[(mstatus.name, mstatus.value) for mstatus in MaritalStatus],
                        render_kw={"placeholder":"Marital Status", "class":"form-control form-select", "required":"required"})    
    id_number = StringField("ID Number", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"ID Number", "class":"form-control", "required":"required"})
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=30)],
                       render_kw={"placeholder":"Phone Number", "type":"tel", "class":"form-control", "required":"required"})
    email = StringField("Email Address", validators=[Length(max=100)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control"})
    dependants = IntegerField("Dependants", render_kw={"placeholder":"Dependants", "class":"form-control"})
    address = TextAreaField("Postal Address", validators=[Length(max=150)],
                       render_kw={"placeholder":"Postal Address", "class":"form-control"})
    location = TextAreaField("Physical Location", validators=[Length(max=150)],
                       render_kw={"placeholder":"Physical Location", "class":"form-control"})
    nearest_landmark = TextAreaField("Nearest Landmark", validators=[Length(max=150)],
                       render_kw={"placeholder":"Nearest Landmark", "class":"form-control"})
    house_status = SelectField("House Status", choices=[(house.name, house.value) for house in HouseStatus],
                        render_kw={"placeholder": "House Status", "class": "form-control form-select"})
    estate_apartment = TextAreaField("Estate|Apartment", validators=[Length(max=100)],
                       render_kw={"placeholder":"Estate|Aparment", "class":"form-control"})
    house_number = StringField("House Number", validators=[Length(max=100)],
                       render_kw={"placeholder":"House Number", "class":"form-control"})
    next_of_kin = StringField("Name of Next of Kin", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder": "Name of Next of Kin", "type":"text", "class": "form-control", "required":"required"})
    kin_phone = StringField("Kin Phone Number", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"Kin Phone Number", "type":"tel", "class":"form-control", "required":"required"})
    kin_id = StringField("Kin ID Number", validators=[Length(max=20)],
                       render_kw={"placeholder":"Kin ID Number", "class":"form-control"})
    registration_fee = FloatField("Registration Fee", validators=[DataRequired()],
                       render_kw={"placeholder":"Registration", "type":"number", "class":"form-control", "required":"required"})
    mode_of_payment = SelectField("Mode of Payment", choices=[(mode.name, mode.value) for mode in ModeOfPayment],
                        render_kw={"placeholder": "Saving Status", "class": "form-control form-select", "required":"required"})
    transaction_code = StringField("Transaction Code", render_kw={"placeholder": "Transaction Code", "class":"form-control"})
    status = SelectField("Member Status", choices=[(status.name, status.value) for status in MemberStatus],
                        render_kw={"placeholder": "Member Status", "class": "form-control form-select"})
#========================================================================================#


#========================================================================================#
# GPS Coordinates Form
#========================================================================================#
class CoordinatesForm(FlaskForm):
    """GPS Coordinates form defination"""
    gps_latitude = FloatField("GPS Latitude", validators=[DataRequired()],
                       render_kw={"placeholder":"GPS Latitude", "class":"form-control", "required":"required"})
    gps_longitude = FloatField("GPS Longitude", validators=[DataRequired()],
                       render_kw={"placeholder":"GPS Longitute", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Attachments Form
#========================================================================================#
class AttachmentsForm(FlaskForm):
    """Attachments form defination"""
    amount = FloatField("Amount", validators=[DataRequired()],
                       render_kw={"placeholder":"Amount", "type":"number", "class":"form-control", "required":"required"})
    penalty = FloatField("Penalty", validators=[DataRequired()],
                       render_kw={"placeholder":"Penalty", "type":"number", "class":"form-control"})
    date_paid = DateField("Date Paid", validators=[DataRequired()],
                       render_kw={"placeholder":"Due Date", "type":"date", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Savings Form
#========================================================================================#
class SavingsForm(FlaskForm):
    """Savings form defination"""
    member_id = SelectField("Member", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Member", "class":"form-control form-select", "required":"required"})
    amount = FloatField("Amount", validators=[DataRequired()],
                       render_kw={"placeholder":"Amount", "type":"number", "class":"form-control", "required":"required"})
    mode_of_payment = SelectField("Mode of Payment", choices=[(mode.name, mode.value) for mode in ModeOfPayment],
                        render_kw={"placeholder": "Saving Status", "class": "form-control form-select", "required":"required"})
    transaction_code = StringField("Transaction Code", render_kw={"placeholder": "Transaction Code", "class":"form-control"})
    transaction_date = DateField("Transaction Date", validators=[DataRequired()],
                       render_kw={"placeholder":"Transaction Date", "type":"date", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Loan Forms
#========================================================================================#
class LoanForm(FlaskForm):
    """Loan form defination"""
    member_id = SelectField("Member", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Member", "class":"form-control form-select", "required":"required"})
    loantype_id = SelectField("Loan Type", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Loan Type", "class":"form-control form-select", "required":"required"})
    rate = FloatField("Rate", validators=[DataRequired()],
                       render_kw={"placeholder":"Rate", "type":"number", "class":"form-control", "required":"required"})
    amount = FloatField("Amount", validators=[DataRequired()],
                       render_kw={"placeholder":"Amount", "type":"number", "class":"form-control", "required":"required"})
    amount_in_words = TextAreaField("Amount in Words", validators=[DataRequired(), Length(max=150)],
                       render_kw={"placeholder":"Amount in Words", "type":"text", "class":"form-control", "required":"required"})
    processing_fee = FloatField("Processing Fee", validators=[DataRequired()],
                       render_kw={"placeholder":"Processing Fee", "type":"number", "class":"form-control", "required":"required"})
    application_date = DateField("Application Date", validators=[DataRequired()],
                       render_kw={"placeholder":"Application Date", "type":"date", "class":"form-control", "required":"required"})
    due_date = DateField("Due Date", validators=[DataRequired()],
                       render_kw={"placeholder":"Due Date", "type":"date", "class":"form-control", "required":"required"})
    installments = FloatField("Installments in Weeks", validators=[DataRequired()],
                       render_kw={"placeholder":"Installments in Weeks", "type":"number", "class":"form-control", "required":"required"})
    status = SelectField("Loan Status", choices=[(status.name, status.value) for status in LoanStatus],
                        render_kw={"placeholder": "Loan Status", "class": "form-control form-select"})
#========================================================================================#


#========================================================================================#
# Repayments Form
#========================================================================================#
class RepaymentForm(FlaskForm):
    """Repayments form defination"""
    amount = FloatField("Amount", validators=[DataRequired()],
                       render_kw={"placeholder":"Amount", "type":"number", "class":"form-control", "required":"required"})
    penalty = FloatField("Penalty", render_kw={"placeholder":"Penalty", "class":"form-control"})
    mode_of_payment = SelectField("Mode of Payment", choices=[(mode.name, mode.value) for mode in ModeOfPayment],
                        render_kw={"placeholder": "Saving Status", "class": "form-control form-select", "required":"required"})
    transaction_code = StringField("Transaction Code", render_kw={"placeholder": "Transaction Code", "class":"form-control"})
    date_paid = DateField("Date Paid", validators=[DataRequired()],
                       render_kw={"placeholder":"Due Date", "type":"date", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Collateral Form
#========================================================================================#
class CollateralForm(FlaskForm):
    """Collateral form defination"""
    loan_id = SelectField("Loan", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Loan", "class":"form-control form-select", "required":"required"})
    name = StringField("Name", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Name", "type":"text", "class": "form-control", "required":"required"})
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=200)],
                       render_kw={"placeholder":"Description", "class":"form-control", "required":"required"})
    value = FloatField("Value", validators=[DataRequired()],
                       render_kw={"placeholder":"Value", "type":"number", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Business Forms
#========================================================================================#
class BusinessForm(FlaskForm):
    """Business form defination"""
    loan_id = SelectField("Loan", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Loan", "class":"form-control form-select", "required":"required"})
    name = StringField("Name", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Name", "type":"text", "class": "form-control", "required":"required"})
    business_type = StringField("Business Type", validators=[DataRequired()],
                        render_kw={"placeholder":"Business Type", "class":"form-control", "required":"required"})
    address = TextAreaField("Postal Address", validators=[DataRequired(), Length(max=150)],
                       render_kw={"placeholder":"Postal Address", "class":"form-control", "required":"required"})
    location = TextAreaField("Business Location", validators=[DataRequired(), Length(max=150)],
                       render_kw={"placeholder":"Business Location", "class":"form-control", "required":"required"})
    building = StringField("Building", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Building", "class":"form-control", "required":"required"})
    town = StringField("Town", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Town", "class":"form-control", "required":"required"})
    street = StringField("Street", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Street", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Guarantor Forms
#========================================================================================#
class GuarantorForm(FlaskForm):
    """Guarantor form defination"""
    loan_id = SelectField("Loan", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Loan", "class":"form-control form-select", "required":"required"})
    name = StringField("Name", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Name", "type":"text", "class": "form-control", "required":"required"})
    gender = SelectField("Gender", choices=[(gender.name, gender.value) for gender in Gender],
                        render_kw={"placeholder":"Gender", "class":"form-control form-select", "required":"required"})  
    id_number = StringField("ID Number", validators=[DataRequired(), Length(max=10)],
                       render_kw={"placeholder":"ID Number", "class":"form-control", "required":"required"})
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"Phone Number", "type":"tel", "class":"form-control", "required":"required"})
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    address = TextAreaField("Postal Address", validators=[DataRequired(), Length(max=150)],
                       render_kw={"placeholder":"Postal Address", "class":"form-control", "required":"required"})
    location = TextAreaField("Physical Location", validators=[DataRequired(), Length(max=150)],
                       render_kw={"placeholder":"Physical Location", "class":"form-control", "required":"required"})
    consent = BooleanField("Guarantor Consent?", render_kw={"placeholder":"Consent", "type":"checkbox", "class":"form-check-input"})
#========================================================================================#



#----------------------------------------------------------------------------------------#
# Settings View Forms Ends Here
#========================================================================================#