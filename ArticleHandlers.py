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