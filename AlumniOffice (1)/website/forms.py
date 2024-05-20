from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class AlumniProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    school = StringField('School', validators=[DataRequired(), Length(min=2, max=100)])
    graduation_year = IntegerField('Graduation Year', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])