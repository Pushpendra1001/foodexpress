from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=50, message="Username must be between 3 and 50 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    address = StringField('Address', validators=[
        DataRequired(message="Address is required"),
        Length(min=10, message="Address must be at least 10 characters long")
    ])
    contact = StringField('Contact Number', validators=[
        DataRequired(message="Contact number is required"),
        Length(min=10, max=15, message="Please enter a valid contact number")
    ])

class CheckoutForm(FlaskForm):
    delivery_option = RadioField(
        'Delivery Option',
        choices=[
            ('express', 'Express Delivery'),
            ('standard', 'Standard Delivery'),
            ('pickup', 'Store Pickup')
        ],
        validators=[DataRequired(message="Please select a delivery option")]
    )
    address = StringField('Delivery Address', validators=[
        DataRequired(message="Address is required"),
        Length(min=10, message="Address must be at least 10 characters long")
    ])
    contact = StringField('Contact Number', validators=[
        DataRequired(message="Contact number is required"),
        Length(min=10, max=15, message="Please enter a valid contact number")
    ])
    special_instructions = TextAreaField('Special Instructions')