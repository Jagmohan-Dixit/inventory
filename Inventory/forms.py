from flask_wtf import FlaskForm
import os
from flask import json
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