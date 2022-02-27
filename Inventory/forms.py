from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired
from wtforms import StringField, SubmitField, PasswordField,  SelectField, EmailField, DateField, IntegerField


dr = DataRequired()


class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[dr], render_kw={"placeholder":"Email"})
    password = PasswordField("Password", validators=[dr], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")


class AdditemForm(FlaskForm):

    issuedfrom = StringField("from", validators=[dr])
    productname = StringField("productname", validators=[dr])
    date = DateField("date", validators=[dr])
    dateofsurvey = DateField("dateofsurvey", validators=[dr])
    billno = StringField("billno", validators=[dr])
    nameoffirm = StringField("nameoffirm", validators=[dr])
    itemno = StringField("itemno", validators=[dr])
    quantity = IntegerField("quantity", validators=[dr])
    rateperitem = StringField("rateperitem", validators=[dr])
    totalamount = StringField("totalamount", validators=[dr])
    crvno = StringField("crvno", validators=[dr])
    submit = SubmitField("Add")

class IssuedForm(FlaskForm):

    issuedfrom = StringField("issuedfrom", validators=[dr])
    issuedto = StringField("issuedto", validators=[dr])
    district = StringField("district", validators=[dr])
    quantity = IntegerField("quantity", validators=[dr])
    submit = SubmitField("Assign")

class AddStation(FlaskForm):

    station = StringField('Station', validators=[dr])
    district = SelectField('District',validators=[dr], choices=[])
    submit = SubmitField("Add Station")


class SearchForm(FlaskForm):
    search = StringField("search",  render_kw={"placeholder":"Search inventory..."})

