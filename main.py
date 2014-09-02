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
from Handler import *
import re
import Database
import json
from MemberHandlers import *
from ArticleHandlers import *
from CarouselHandlers import *
from CalendarHandlers import *

class MainHandler(Handler):
	def get(self):
		articles = Database.get_all_articles()
		articles.sort(reverse=True, key=lambda r: r.datetime_created)
		front_articles = []
		num_articles = 5
		if len(articles) < 5:
			num_articles = len(articles)
		for i in range(num_articles):
			front_articles.append(articles[i])

		slides = Database.get_all_carousel_slides()
		self.render('home.html', articles=front_articles, slides=slides)

class LoginPageHandler(Handler):
	def get(self):
		self.render('login.html')

class LoginHandler(Handler):
	def get(self):
		pass
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		if (Database.valid_password(username, password)):
			self.login(Database.get_user(username))
			self.response.out.write("Success")
		else:
			self.response.out.write("Failure")

class LogoutHandler(Handler):
	def get(self):
		self.logout()
		self.redirect('/')

class RegisterHandler(Handler):
	def get(self):
		pass
	def post(self):
		username_is_taken = False
		passwords_dont_match = False
		username_is_invalid = False
		email_is_invalid = False

		username = self.request.get('username')
		password = self.request.get('password')
		password_repeat = self.request.get('password-repeat')
		email = self.request.get('email')
		first_name = self.request.get('first-name')
		last_name = self.request.get('last-name')

		username_is_taken = username in Database.get_all_users()
		passwords_dont_match = password != password_repeat
		username_is_invalid = re.match("^[a-zA-Z0-9_-]{3,20}$", username) is None
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			email_is_invalid = True
		if username_is_taken or passwords_dont_match or username_is_invalid or email_is_invalid:
			s = "Failure"
			if username_is_taken:
				s += " username_is_taken"
			if passwords_dont_match:
				s += " passwords_dont_match"
			if username_is_invalid:
				s += ' username_is_invalid'
			if email_is_invalid:
				s += ' email_is_invalid'
			self.response.out.write(s)
		else:
			Database.add_user(first_name, last_name, username, password, email)
			self.login(Database.get_user(username))
			self.response.out.write("Success")

class GetUserHandler(Handler):
	def get(self):
		query_list = self.request.query_string.split('=')
		user = None
		if len(query_list) < 2:
			user = self.get_user()
		else:
			username = query_list[1]
			user = Database.get_user(username)
		if not user:
			return
		# TODO
		obj = json.dumps({"username":user.username, "permissions":user.permissions})
		self.response.out.write(str(obj))

class AboutHandler(Handler):
	def get(self):
		self.render('about.html')

class GettingInvolvedHandler(Handler):
	def get(self):
		self.render('gettinginvolved.html')

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/calendar', CalendarHandler),
	('/about', AboutHandler),
	('/about/gettinginvolved', GettingInvolvedHandler),
	('/members', MembersHandler),
	('/members/moderator', ModeratorHandler),
	('/members/articles', ArticlesHandler),
	('/members/carousel', CarouselHandler),
	('/login', LoginPageHandler),
	('/logout', LogoutHandler),
	('/control/login', LoginHandler),
	('/control/register', RegisterHandler),
	('/control/getuser', GetUserHandler),
	('/control/getevents', GetEventsHandler)
], debug=True)
