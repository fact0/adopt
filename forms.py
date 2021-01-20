from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES
from wtforms import FloatField, BooleanField, IntegerField, RadioField, SelectField, TextAreaField, StringField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length
DEFAULT_IMAGE = 'https://files.catbox.moe/oo5ikc.jpg'


class MyInputRequired(InputRequired):
    field_flags = ()


class PetForm(FlaskForm):
    """Form for adding pets"""
    images = UploadSet('images', IMAGES)

    name = StringField("Pet Name", validators=[
                       MyInputRequired(message="Pet Name cannot be blank")])
    species = SelectField("Pet Species", choices=[
        ('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    age = IntegerField("Pet Age", validators=[
                       Optional(), NumberRange(min=1, max=30, message=("Please enter a valid age from 0 to 30"))])
    photo_url = StringField("Pet Photo URL", validators=[
                            Optional(strip_whitespace=True,), URL(message="Please enter a valid URL")])
    photo = FileField('image', validators=[Optional(strip_whitespace=True,), FileAllowed(images, 'Images only!')
                                           ])
    notes = TextAreaField("Enter notes about pet", validators=[
                          Optional(), Length(min=10, message="Please Enter more than 10 characters")])
    available = BooleanField("Is this pet available?")


# filters=[lambda x: x or DEFAULT_IMAGE]
