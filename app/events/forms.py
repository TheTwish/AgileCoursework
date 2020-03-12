from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange

class AddEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=50)])
    host = StringField('Host', validators=[DataRequired(), Length(min=2, max=50)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=100, max=5000)])
    image = FileField('Add image', validators=[FileAllowed(['jpg', 'png'])])
    price = DecimalField('Price', default=0.00)
    #date = DateField("Pick A Date",format='%d-%m-%Y' )
    #category_id = SelectField('Select category', coerce=int)
    submit = SubmitField('Add event')

class EditEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=50)])
    host = StringField('Host', validators=[DataRequired(), Length(min=2, max=50)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=100, max=5000)])
    image = FileField(
        'Update event image - <span style="color:red;">only replace if old or incorrect</span>', 
        validators=[
            FileAllowed(['jpg', 'png'], 'Images only with extension .jpg or .png')
        ]
    )
    price = DecimalField('Price', default=0.00)
    #category_id = SelectField('Category', coerce=int)
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')

class ReviewForm(FlaskForm):
    rating = DecimalField(default=0.0, validators=[NumberRange(min=0, max=5)])
    text = TextAreaField('Write a review')
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=22)])
    submit = SubmitField('Submit')

class EditCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=22)])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')