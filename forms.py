from flask_wtf import FlaskForm
from wtforms import FloatField, BooleanField, IntegerField, RadioField, SelectField, TextAreaField, StringField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length
DEFAULT_IMAGE = 'https://files.catbox.moe/oo5ikc.jpg'


class MyInputRequired(InputRequired):
    field_flags = ()


class PetForm(FlaskForm):
    """Form for adding pets"""

    name = StringField("Pet Name", validators=[
                       MyInputRequired(message="Pet Name cannot be blank")])
    species = SelectField("Pet Species", choices=[
        ('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    age = IntegerField("Pet Age", validators=[
                       Optional(), NumberRange(min=1, max=30, message=("Please enter a valid age from 0 to 30"))])
    photo_url = StringField("Pet Photo URL", filters=[lambda x: x or DEFAULT_IMAGE], validators=[
                            Optional(strip_whitespace=True,), URL(message="Please enter a valid URL")])
    notes = TextAreaField("Enter notes about pet", validators=[
                          Optional(), Length(min=10, message="Please Enter more than 10 characters")])
    available = BooleanField("Is this pet available?")
