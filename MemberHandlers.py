from Handler import *
import re
import Database
import json

class MembersHandler(Handler):
	def get(self):
		user = self.get_user()
		if user:
			self.render('member.html')
		else:
			self.redirect('/login')

class ModeratorHandler(Handler):
	def get(self):
		self.render('moderator.html', users = Database.get_all_users())
	def post(self):
		username = self.request.get('username')
		bio_is_displayed = self.request.get('bio_is_displayed')
		is_a_moderator = self.request.get('is_a_moderator')
		can_create_news_posts = self.request.get('can_create_news_posts')
		can_edit_news_posts = self.request.get('can_edit_news_posts')
		can_claim_workshops = self.request.get('can_claim_workshops')
		can_free_workshops = self.request.get('can_free_workshops')
		can_cancel_workshops = self.request.get('can_cancel_workshops')
		can_edit_homepage = self.request.get('can_edit_homepage')
		Database.set_permissions(username, bio_is_displayed=bio_is_displayed,
										is_a_moderator=is_a_moderator,
										can_create_news_posts=can_create_news_posts,
										can_edit_news_posts=can_edit_news_posts,
										can_claim_workshops=can_claim_workshops,
										can_free_workshops=can_free_workshops,
										can_cancel_workshops=can_cancel_workshops,
										can_edit_homepage=can_edit_homepage)
		self.render('moderator.html', users = Database.get_all_users())
