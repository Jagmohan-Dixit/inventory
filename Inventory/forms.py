from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField,  SelectField, EmailField, DateField, IntegerField


dr = DataRequired()


class LoginForm(FlaskForm):

    email = EmailField("Email", validators=[dr], render_kw={"placeholder":"Email"})
    password = PasswordField("Password", validators=[dr], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):

    email = EmailField("Email", validators=[dr], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[dr, EqualTo('cfPassword', message='Password Must Match')], render_kw={"placeholder": "Password"})
    cfPassword = PasswordField("Confirm Password", validators=[dr], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")


class AdditemForm(FlaskForm):

    productname = StringField("productname", validators=[dr])
    dateofsurvey = DateField("dateofsurvey", validators=[dr])
    billno = StringField("billno", validators=[dr])
    nameoffirm = StringField("nameoffirm", validators=[dr])
    quantity = IntegerField("quantity", validators=[dr])
    rateperitem = StringField("rateperitem", validators=[dr])
    totalamount = StringField("totalamount", validators=[dr])
    submit = SubmitField("Add")


class SearchForm(FlaskForm):
    search = StringField("search",  render_kw={"placeholder":"Search inventory..."})



















# site_root = os.path.realpath(os.path.dirname(__file__))
# filename = os.path.join(site_root,'static/jsondata','data.json')
# data = None
# with open(filename) as test_file:
#     data = json.load(test_file)

# dist = []
# districts = data['districts']
# for i in districts[0]:
#     dist.append(i)
#     for j in districts[0][i]:
#         print(j)