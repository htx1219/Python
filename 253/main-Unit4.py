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
import hmac
import random
import string
import hashlib
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

SECRET = 'ltbl'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)

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

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.EmailProperty
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_front(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("show_blog.html", blogs=blogs)
    def get(self):
        self.render_front()

class NewPost(Handler):
    def render_front(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error = error)
    def get(self):
        self.render_front()
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            a = Blog(subject=subject, content=content)
            a.put()
            self.redirect("/blog/%(id)s" % {"id":a.key().id()})
        else:
            error = "we need both a subject and some content!"
            self.render_front(subject, content, error)

class Permalink(MainPage):
    def get(self, blog_id):
        s = Blog.get_by_id(int(blog_id))
        self.render("show_blog.html", blogs=[s])

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("signup-form.html")
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if User.all().filter('username =', username).get():
            params['error_username'] = "This user already exists."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            password_hash = make_pw_hash(username, password)
            a = User(username=username, password=password_hash, email=email)
            a.put()
            user_id = a.key().id()
            user_id_hash = make_secure_val(str(user_id))
            self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % user_id_hash)
            self.redirect('/blog/welcome')

class Login(Handler):
    def get(self):
        self.render("login-form.html")
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        if User.all().filter('username =', username).get():
            user = User.all().filter('username =', username).get()
            if valid_pw(username, password, user.password):
                user_id = user.key().id()
                user_id_hash = make_secure_val(str(user_id))
                self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % user_id_hash)
                self.redirect('/blog/welcome')
        self.render('login-form.html',**{"error_message" : "Invalid username or password"})

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/blog/signup')
        
class Welcome(Handler):
    def get(self):
        user_id_hash = self.request.cookies.get('name',0)
        user_id = check_secure_val(user_id_hash)
        if check_secure_val(user_id_hash):
            user = User.get_by_id(int(user_id))
            username = user.username
            self.render('welcome.html', username = username)
        else:
            self.redirect('/blog/signup')

app = webapp2.WSGIApplication([('/blog', MainPage),
                               ('/blog/newpost', NewPost),
                               (r'/blog/(\d+)', Permalink),
                               ('/blog/signup', Signup),
                               ('/blog/welcome', Welcome),
                               ('/blog/login', Login),
                               ('/blog/logout', Logout)],
                              debug=True)
