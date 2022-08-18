from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Regexp, Length
#
# class Form(FlaskForm):
#     country = SelectField("country",
#                         choices= [('United States' ,'United States'),
#                                   ('Belgium','Belgium'),
#                                   ('Russian Federation', 'Russian'),
#                                   ('Japan', 'Japan')])
#     activity_group = SelectField("activity_group",
#                         choices=[('combustible_fuel', 'fuel'),
#                                    ('consumption', 'consumption'),
#                                    ('energy', 'energy'),
#                                    ('ownuse', 'ownuse')])
#     submit = SubmitField('Predict')

# User Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), InputRequired(), Length(min=5, max=10, message='Username must be between 5-10 characters long'), Regexp('^[A-Za-z\\d]+$')]) # required
    password = PasswordField('Password', validators=[DataRequired(), InputRequired(), Length(min=4, max=15, message='Password must be between 4-15 characters long'), Regexp('^[A-Za-z\\d]+$')]) # required
    submit = SubmitField('Login')

# User Signup
class SignupForm(FlaskForm):
    username = StringField('Username (only letters and numbers accepted)', validators=[DataRequired(), InputRequired(), Length(min=5, max=10, message='Username must be between 5-10 characters long'), Regexp('^[A-Za-z\\d]+$')]) # required, only alphabetic letters and numbers
    password = PasswordField('Password (only letters and numbers accepted)', validators=[DataRequired(), InputRequired(), Length(min=4, max=15, message='Password must be between 4-15 characters long'), Regexp('^[A-Za-z\\d]+$')]) # required, only alphabetic letters and numbers
    verify = PasswordField('Verify Password', validators=[DataRequired(), InputRequired()]) # required
    submit = SubmitField('Signup')

# User Update
class UpdateForm(FlaskForm):
    username = StringField('New username (only letters and numbers accepted)', validators=[DataRequired(), InputRequired(), Length(min=5, max=10, message='Username must be between 5-10 characters long'), Regexp('^[A-Za-z\\d]+$')]) # required, only alphabetic letters and numbers
    submit = SubmitField('Update')

# https://wtforms.readthedocs.io/en/3.0.x/validators/?highlight=numberrange#wtforms.validators