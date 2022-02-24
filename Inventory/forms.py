from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, EmailField, DateTimeLocalField, HiddenField
from flask_wtf.file import FileField, FileAllowed


dr = DataRequired()

class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[dr], render_kw={"placeholder":"Email"})
    password = PasswordField("Password", validators=[dr], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

class AdditemForm(FlaskForm):

    issuedfrom = StringField("from", validators=[dr])
    productname = StringField("productname", validators=[dr])
    date = StringField("date", validators=[dr])
    dateofsurvey = StringField("dateofsurvey", validators=[dr])
    billno = StringField("billno", validators=[dr])
    nameoffirm = StringField("nameoffirm", validators=[dr])
    itemno = StringField("itemno", validators=[dr])
    quantity = StringField("quantity", validators=[dr])
    rateperitem = StringField("rateperitem", validators=[dr])
    totalamount = StringField("totalamount", validators=[dr])
    crvno = StringField("crvno", validators=[dr])
    submit = SubmitField("Assign")

class IssuedForm(FlaskForm):

    issuedfrom = StringField("issuedfrom", validators=[dr])
    issuedto = StringField("issuedto", validators=[dr])
    district = StringField("district", validators=[dr])
    quantity = StringField("quantity", validators=[dr])
    submit = SubmitField("Assign")


class SearchForm(FlaskForm):
    search = StringField("search", validators=[dr], render_kw={"placeholder":"Search inventory..."})


class User(FlaskForm):
    name = StringField()
    password = StringField()
    email = StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)