from Handler import *
import re
import Database
import json

class CarouselHandler(Handler):
	def get(self):
		user = self.get_user()
		if user:
			self.render('carousel.html')
		else:
			self.redirect('/login')

	def post(self):
		user = self.get_user()
		if user:
			image_url = self.request.get('image-url')
			title = self.request.get('title')
			description = self.request.get('description')
			button_text = self.request.get('button-text')
			button_url = self.request.get('button-url')	

			Database.add_carousel_slide(title, description, image_url, button_text, button_url)
			self.render('carousel.html')
		else:
			self.redirect('/login')		

