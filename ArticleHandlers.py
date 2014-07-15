from Handler import *
import re
import Database
import json

class ArticlesHandler(Handler):
	def get(self):
		user = self.get_user()
		if user:
			self.render('articles.html')
		else:
			self.redirect('/login')

	def post(self):
		user = self.get_user()
		if user:
			heading = self.request.get('heading')
			summary = self.request.get('summary')
			content = self.request.get('content')
			image_url = self.request.get('image-url')
			Database.add_article(heading, summary, content, image_url)
			self.render('articles.html')
		else:
			self.redirect('/login')		

