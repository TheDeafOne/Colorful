from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional


# define our own FlaskForm subclass for our form
class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    username = StringField("Display Name: ", validators=[InputRequired()])
    password = PasswordField("Password: ",
                             validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ",
                                     validators=[EqualTo('password')])
    submit = SubmitField("Register")

# define our own FlaskForm subclass for our form


class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ",
                             validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    email = EmailField("Email: ", validators=[Optional(), Email()])
    username = StringField("Display Name: ", validators=[Optional()])
    old_password = PasswordField("Old Password: ",
                                 validators=[Optional()])
    new_password = PasswordField("New Password: ",
                                 validators=[Optional(), Length(min=8, max=256)])
    confirm_new_password = PasswordField("New Password: ",
                                         validators=[Optional(), Length(min=8, max=256)])
    submit = SubmitField("Register")
