#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def escape_html(s):
    return cgi.escape(s, quote=True)

form = """
<form method="post">
    What is your birthday?
    <br>
    <label> Month <input type = "text" name="month" value = "%(month)s"></label>
    <label> Day <input type = "text" name="day" value = %(day)s></label>
    <label> Year <input type = "text" name="year" value = %(year)s></label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type = "submit"><br>
    <a href = "/rot13"> try out the rot13 code!</a>
    <br><br>
    <a href = "/signup"> Why not sign up for our website!</a>
</form>
"""

form13 = """
<form method = "post">
    <h2>Enter some text to ROT13:</h2>
    <br>
    <textarea name="text"
                style="height: 100px; width: 400px;">
%(rot13text)s
    </textarea>
    <br>
    <input type = "submit">
</form>
"""

formsignup="""
<h2>Signup</h2><br>
<form method = "post">
    Username <input type ="text" name= "username" value = "%(username)s">
    <div style="color: red">%(error1)s</div><br>
    Password <input type = "password" name = "password">
    <div style="color: red">%(error2)s</div><br>
    Verify Password<input type = "password" name="verify">
    <div style="color: red">%(error3)s</div><br>
    Email(optional) <input type ="text" name= "email" value = "%(email)s">
    <div style="color: red">%(error4)s</div>
    <br>
    <input type = "submit">
</form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if months:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        return int(day) if int(day) in range(1,32) else None

def valid_year(year):
    if year and year.isdigit():
        return int(year) if int(year) in range(1900, 2020) else None

class MainPage(webapp2.RequestHandler):
    
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error":error,
                                        "month":escape_html(month),
                                        "day":escape_html(day),
                                        "year":escape_html(year)})
    
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)
        
        if not (month and day and year):
            self.write_form("That's doesn't look valid for me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks, that's a totally valid date!")

def rot13(string):
    q = "abcdefghijklmnopqrstuvwxyz"
    dictn = [(q[i], q[(i+13)%26]) for i in range(26)]
    d = dict(dictn)
    result = ""
    for i in string:
        if i in d:
            result = result+d[i]
        elif i.lower() in d:
            result = result+d[i.lower()].upper()
        else:
            result = result+i
    return result

class Rot13Handler(webapp2.RequestHandler):
    
    def write_form(self, text13 = ""):
        self.response.out.write(form13 % {"rot13text":text13})

    def get(self):
        self.write_form()

    def post(self):
        user_rottext = self.request.get('text')
        self.write_form(escape_html(rot13(user_rottext)))

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_re = re.compile("^.{3,20}$")
email_re = re.compile("^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return user_re.match(username)

def valid_password(password):
    return password_re.match(password)

def valid_email(email):
    return email_re.match(email)

class SignupHandler(webapp2.RequestHandler):
    def write_form(self, username="", email="", error1="", error2="", error3="", error4=""):
        self.response.out.write(formsignup % {"username":escape_html(username),
                                              "email":escape_html(email),
                                              "error1":error1,
                                              "error2":error2,
                                              "error3":error3,
                                              "error4":error4})
    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        
        if not valid_username(user_username):
            error1 = "That's not a valid username."
        else:
            error1 = ""
            
        if not valid_password(user_password):
            error2 = "That's not a valid password"
            error3 = ""
        elif user_password != user_verify:
            error2 = ""
            error3 = "Your passwords didn't match."
        else:
            error2 = ""
            error3 = ""
        if not user_email:
            error4 = ""
        elif not valid_email(user_email):
            error4 = "That's not a valid email"
        else:
            error4 = ""
        if (error1 == "" and error2 == "" and error3 == "" and error4 == ""):
            self.redirect('/welcome?username=%s' %user_username)
        else:
            self.write_form(user_username, user_email, error1, error2, error3, error4)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('username')
        self.response.out.write("Welcome! %s!" % user_name)
        

##class TestHandler(webapp2.RequestHandler):
##    def post(self):
##        q = self.request.get("q")
##        self.response.out.write(q)
##        
##        self.response.headers['Content-Type'] = 'text/plain'
##        self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler),
                               ('/rot13', Rot13Handler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler)],
                              debug=True)
#,                              ('/testform', TestHandler)
