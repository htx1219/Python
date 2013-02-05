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
import json
import time
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
        params['user'] = self.user
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('name')
        self.user = uid and User.get_by_id(int(uid))

def escape_html(s):
    return cgi.escape(s, quote=True)

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Wiki(db.Model):
    address = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.EmailProperty
    created = db.DateTimeProperty(auto_now_add = True)

class WikiPage(Handler):
    def get(self, address):
        wiki = Wiki.gql("WHERE address = :1 ORDER BY created DESC LIMIT 1", address).get()
        if not wiki:
            if address == '/':
                a = Wiki(address=address, content="<h1>Welcome to my Wiki<h1>")
                a.put()
                self.redirect("/wiki/")
            else:
                self.redirect("/wiki/_edit%s" % address)
        self.render("wikipage.html", address=address, wiki=wiki)

class EditPage(Handler):
    def get(self, address):
        if not self.user:
            self.redirect("/wiki/login")
        wiki = Wiki.gql("WHERE address = :1 ORDER BY created DESC LIMIT 1", address).get()
        self.render("editwiki.html", wiki=wiki, address=address)

    def post(self, address):
        wiki = Wiki.gql("WHERE address = :1 ORDER BY created DESC LIMIT 1", address).get()
        content = self.request.get("content")
        if content:
            a = Wiki(address=address, content=content)
            a.put()
            self.redirect("/wiki%s" % address)
        else:
            error = "we need some content!"
            self.render("editwiki.html", error=error, wiki=wiki, address=address)

CACHE = {}
def blog_cache_query(s, update = False):
    if not update and s in CACHE:
        res = CACHE[s]
    else:
        if isinstance(s, str):
            ans = db.GqlQuery(s)
        elif isinstance(s, int):
            ans = Blog.get_by_id(s)
        res = (ans, time.gmtime())
        CACHE[s] = res
    return res

class MainPage(Handler):
    def render_front(self, qtime=0):
        ans = blog_cache_query("SELECT * FROM Blog ORDER BY created DESC limit 10")
        qtime=time.mktime(time.gmtime())-time.mktime(ans[1])
        self.render("show_blog.html", blogs=ans[0], qtime=qtime)
    def get(self):
        self.render_front()

class MainPageJson(Handler):
    def get(self):
        blogs = blog_cache_query("SELECT * FROM Blog ORDER BY created DESC limit 10")[0]
        w = []
        for b in blogs:
            q = {}
            q["subject"] = b.subject
            q["content"] = b.content
            q["created"] = b.created.strftime('%a %b  %d %H:%M:%S %Y')
            w.append(q)
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(w))

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
            del CACHE["SELECT * FROM Blog ORDER BY created DESC limit 10"]
            self.redirect("/blog/%(id)s" % {"id":a.key().id()})
        else:
            error = "we need both a subject and some content!"
            self.render_front(subject, content, error)

class Permalink(MainPage):
    def get(self, blog_id):
        ans = blog_cache_query(int(blog_id))
        qtime=time.mktime(time.gmtime())-time.mktime(ans[1])
        self.render("show_blog.html", blogs=[ans[0]], qtime = qtime)

class PermalinkJson(MainPage):
    def get(self, blog_id):
        self.response.headers['Content-Type'] = 'application/json'
        s = blog_cache_query(int(blog_id))[0]
        q = {}
        q["subject"] = s.subject
        q["content"] = s.content
        q["created"] = s.created.strftime('%a %b  %d %H:%M:%S %Y')
        self.write(json.dumps(q))

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
    def post_to_des(self, des):
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
            self.redirect(des)

class BlogSignup(Signup):
    def post(self):
        self.post_to_des('/blog/welcome')

class WikiSignup(Signup):
    def post(self):
        self.post_to_des('/wiki/')

class Login(Handler):
    def get(self):
        self.render("login-form.html")
    def post_to_des(self, des):
        username = self.request.get('username')
        password = self.request.get('password')
        if User.all().filter('username =', username).get():
            user = User.all().filter('username =', username).get()
            if valid_pw(username, password, user.password):
                user_id = user.key().id()
                user_id_hash = make_secure_val(str(user_id))
                self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % user_id_hash)
                self.redirect(des)
        self.render('login-form.html',**{"error_message" : "Invalid username or password"})

class BlogLogin(Login):
    def post(self):
        self.post_to_des('/blog/welcome')

class WikiLogin(Login):
    def post(self):
        self.post_to_des('/wiki/')

class Logout(Handler):
    def get_to_des(self, des):
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect(des)

class BlogLogout(Logout):
    def get(self):
        self.get_to_des('/blog/welcome')

class WikiLogout(Logout):
    def get(self):
        self.get_to_des('/wiki/')

class Flush(Handler):
    def get(self):
        CACHE.clear()
        self.redirect("/blog")

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

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/blog', MainPage),
                               ('/blog/.json', MainPageJson),
                               ('/blog/newpost', NewPost),
                               (r'/blog/(\d+)', Permalink),
                               (r'/blog/(\d+).json', PermalinkJson),
                               ('/blog/signup', BlogSignup),
                               ('/blog/welcome', Welcome),
                               ('/blog/login', BlogLogin),
                               ('/blog/logout', BlogLogout),
                               ('/blog/flush', Flush),
                               ('/wiki/signup', WikiSignup),
                               ('/wiki/login', WikiLogin),
                               ('/wiki/logout', WikiLogout),
                               ('/wiki/_edit' + PAGE_RE, EditPage),
                               ('/wiki'+PAGE_RE, WikiPage),
                               ],
                              debug=True)
