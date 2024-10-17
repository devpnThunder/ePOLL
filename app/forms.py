"""Forms defination file."""
from app.models import Gender
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField, BooleanField, FileField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.models import Permission
from wtforms.validators import DataRequired, Length

#----------------------------------------------------------------------------------------#
# Form defination Start Here

#========================================================================================#
# Auth View Forms Starts Here
#----------------------------------------------------------------------------------------#

#========================================================================================#
# Role Form
#========================================================================================#
class RoleForm(FlaskForm):
    """
    Role form defination
    """
    name = StringField("Role", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder":"Role", "class":"form-control", "required":"required"})
    description = TextAreaField("Description", validators=[Length(max=120)],
                       render_kw={"placeholder": "Description", "type":"text", "class": "form-control"})
    permissions = SelectMultipleField('Permissions', coerce=str,
                                    option_widget=CheckboxInput(),
                                    widget=ListWidget(prefix_label=False))
    
    # permissions = SelectMultipleField("Permissions", coerce=str, validators=[DataRequired()],
    #                     render_kw={"placeholder":"Permissions", "class":"form-control form-select", "style":"height:120px"})
#========================================================================================#



#========================================================================================#
# New Voter Registration Form
#========================================================================================#
class NewVoterForm(FlaskForm):
    """
    New Voter Registration form defination
    """
    constituency_id_id = SelectField("Constituency", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Constituency", "class":"form-control form-select", "required":"required"})
    surname = StringField("Surname", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Surname", "type":"text", "class": "form-control", "required":"required"})
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "First Name", "type":"text", "class": "form-control", "required":"required"})
    othername = StringField("Other Names", validators=[Length(max=20)],
                       render_kw={"placeholder": "Second Name", "type":"text", "class": "form-control"})
    gender = SelectField("Gender", choices=[(gender.name, gender.value) for gender in Gender],
                        render_kw={"placeholder":"Gender", "class":"form-control form-select", "required":"required"})
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
    roles = SelectField("Roles", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Roles", "class":"form-control form-select"})
#========================================================================================#


#========================================================================================#
# Edit Voter Profile Form
#========================================================================================#
class ProfileForm(FlaskForm):
    """
    Edit Voter Profile form defination
    """
    constituency_id_id = SelectField("Constituency", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Constituency", "class":"form-control form-select", "required":"required"})
    surname = StringField("Surname", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "Surname", "type":"text", "class": "form-control", "required":"required"})
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=20)],
                       render_kw={"placeholder": "First Name", "type":"text", "class": "form-control", "required":"required"})
    othername = StringField("Other Names", validators=[Length(max=20)],
                       render_kw={"placeholder": "Second Name", "type":"text", "class": "form-control"})
    gender = SelectField("Gender", choices=[(gender.name, gender.value) for gender in Gender],
                        render_kw={"placeholder":"Gender", "class":"form-control form-select", "required":"required"})
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
#========================================================================================#



#========================================================================================#
# User Form
#========================================================================================#
class UserForm(FlaskForm):
    """
    User Registration form defination
    """
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
    roles = SelectMultipleField('Roles', coerce=str,
                                    option_widget=CheckboxInput(),
                                    widget=ListWidget(prefix_label=False))
    # roles = SelectField("Roles", coerce=str, validators=[DataRequired()],
    #                     render_kw={"placeholder":"Roles", "class":"form-control form-select"})
#========================================================================================#



#========================================================================================#
# Login Form
#========================================================================================#
class LoginForm(FlaskForm):
    """
    User Login form defination
    """
    email = StringField("Email Address", validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder":"Email", "type":"email", "class":"form-control", "required":"required"})
    password = StringField("Password", validators=[DataRequired()],
                       render_kw={"placeholder":"Password", "type":"password", "class":"form-control", "required":"required"})
#========================================================================================#

#----------------------------------------------------------------------------------------#
# Auth View Forms Ends Here
#========================================================================================#





#========================================================================================#
# County and Constituency View Forms Starts Here
#----------------------------------------------------------------------------------------#

#========================================================================================#
# County Form
#========================================================================================#
class CountyForm(FlaskForm):
    """
    County form defination
    """
    name = StringField("Group Name", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder":"Group Name", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Constituency Form
#========================================================================================#
class ConstituencyForm(FlaskForm):
    """
    Constituency form defination
    """
    county_id = SelectField("County", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"County", "class":"form-control form-select", "required":"required"})
    name = StringField("Group Name", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder":"Group Name", "class":"form-control", "required":"required"})
#========================================================================================#

#----------------------------------------------------------------------------------------#
# County and Constituency View Forms Ends Here
#========================================================================================#



#========================================================================================#
# Category|Question|Option|Result View Forms Starts Here
#----------------------------------------------------------------------------------------#
#========================================================================================#
# Category Form
#========================================================================================#
class CategoryForm(FlaskForm):
    """
    Category form defination
    """
    name = StringField("Poll Category", validators=[DataRequired(), Length(max=100)],
                       render_kw={"placeholder":"Poll Category", "class":"form-control", "required":"required"})
#========================================================================================#


#========================================================================================#
# Question Form
#========================================================================================#
class QuestionForm(FlaskForm):
    """
    Question form defination
    """
    text = StringField("Question", validators=[DataRequired(), Length(max=500)],
                       render_kw={"placeholder":"Question", "class":"form-control", "required":"required"})
    country_id = SelectField("County", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"County", "class":"form-control form-select", "required":"required"})
#========================================================================================#



#========================================================================================#
# Option Form
#========================================================================================#
class OptionForm(FlaskForm):
    """
    Option form defination
    """
    question_id = SelectField("Question", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Quetion", "class":"form-control form-select", "required":"required"})
    text = StringField("Question", validators=[DataRequired(), Length(max=500)],
                       render_kw={"placeholder":"Question", "class":"form-control", "required":"required"})
#========================================================================================#



#========================================================================================#
# Result Form
#========================================================================================#
class ResultForm(FlaskForm):
    """
    Result form defination
    """
    option_id = SelectField("Option", coerce=str, validators=[DataRequired()],
                        render_kw={"placeholder":"Option", "class":"form-control form-select", "required":"required"})
    score = IntegerField("Score", validators=[DataRequired()],
                       render_kw={"placeholder":"Score", "type":"number", "class":"form-control", "required":"required"})
#========================================================================================#

#----------------------------------------------------------------------------------------#
# Result View Forms Ends Here
#========================================================================================#
#----------------------------------------------------------------------------------------#
# Question|Option|Result View Forms Ends Here
#========================================================================================#