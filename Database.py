from Handler import *
from google.appengine.ext import ndb
from google.appengine.api import memcache
import hashlib
import random
from string import letters
import datetime

class Reservation(ndb.Model):
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()

	num_tickets = ndb.IntegerProperty()


class Bio(ndb.Model):
	image_url = ndb.StringProperty(required=True)
	description = ndb.TextProperty(required=True)


class MyUser(ndb.Model):
	datetime_created = ndb.DateTimeProperty(required=True, auto_now_add=False)

	first_name = ndb.StringProperty(required=True)
	last_name = ndb.StringProperty(required=True)

	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)

	bio = ndb.StructuredProperty(Bio)

	permissions = ndb.StringProperty(required=True)

	def has_permission(s):
		return s in this.permissions


class CarouselSlide(ndb.Model):
	datetime_created = ndb.DateTimeProperty(required=True, auto_now_add=False)

	image_url = ndb.StringProperty()

	title = ndb.StringProperty()
	description = ndb.StringProperty()

	button_text = ndb.StringProperty()
	button_link = ndb.StringProperty()


class Show(ndb.Model):
	datetime_created = ndb.DateTimeProperty(required=True, auto_now_add=False)

	slide = ndb.StructuredProperty(CarouselSlide)

	max_reservations = ndb.IntegerProperty()
	num_reservations = ndb.IntegerProperty()

class Article(ndb.Model):
	datetime_created = ndb.DateTimeProperty(required=True, auto_now_add=False)
	image_url = ndb.StringProperty()
	heading = ndb.StringProperty(required=True)
	summary = ndb.TextProperty(required=True)
	content = ndb.TextProperty()

# User checks and permissions

def set_permissions(username, bio_is_displayed=False,
								is_a_moderator=False,
								can_create_news_posts=False,
								can_edit_news_posts=False,
								can_claim_workshops=False,
								can_free_workshops=False,
								can_cancel_workshops=False,
								can_edit_homepage=False):

	my_user = get_user(username)
	if not my_user:
		return False

	s = ''
	if bio_is_displayed:
		s += ' bio_is_displayed'
	if is_a_moderator:
		s += ' is_a_moderator'
	if can_create_news_posts:
		s += ' can_create_news_posts'
	if can_edit_news_posts:
		s += ' can_edit_news_posts'
	if can_claim_workshops:
		s += ' can_claim_workshops'
	if can_free_workshops:
		s += ' can_free_workshops'
	if can_cancel_workshops:
		s += ' can_cancel_workshops'
	if can_edit_homepage:
		s += ' can_edit_homepage'

	my_user.permissions = s
	my_user.put()
	# update memcache
	my_users = memcache.get('users')
	cache(my_user)
	return True

def has_permission(username, s):
	my_user = get_user(username)
	if not my_user:
		return False
	return s in my_user.permissions

def username_exists(username):
	return username in memcache.get('users')

def is_registered_user(user, update=False):
	if not user:
		return False
	return username_exists(user.username())

# Articles

def add_article(heading, summary, content, image_url):
	now = datetime.datetime.now()
	article = Article(datetime_created=now, heading=heading, summary=summary)
	if content:
		article.content = content
	if image_url:
		article.image_url = image_url
	article.key = article.put()
	cache(article)

def update_article_cache():
	articles = ndb.gql('SELECT * FROM Article')
	logging.info('Updated article cache.')
	d = {}
	for article in articles:
		d[article.key] = article
	memcache.set('articles', d)

def get_all_articles(update=False):
	articles = memcache.get('articles')
	if update or not articles:
		update_article_cache()
		articles = memcache.get('articles')
	logging.info([articles[article] for article in articles])
	return [articles[article] for article in articles]

def get_article(k):
	articles = memcache.get('articles')
	if not articles:
		update_article_cache()
		articles = memcache.get('articles')
	if not k in articles:
		return None
	return articles[k]

# Carousel Slides

def add_carousel_slide(title, description, image_url, button_text, button_link):
	now = datetime.datetime.now()
	carousel_slide = carousel_slide(datetime_created=now,
									title=title,
									description=description,
									image_url=image_url,
									button_text=button_text,
									button_link=button_link)
	carousel_slide.key = carousel_slide.put()
	cache(carousel_slide)

def update_carousel_slide_cache():
	carousel_slides = ndb.gql('SELECT * FROM CarouselSlide')
	logging.info('Updated carousel_slide cache.')
	d = {}
	for carousel_slide in carousel_slides:
		d[carousel_slide.key] = carousel_slide
	memcache.set('carousel_slides', d)

def get_all_carousel_slides(update=False):
	carousel_slides = memcache.get('carousel_slides')
	if update or not carousel_slides:
		update_carousel_slide_cache()
		carousel_slides = memcache.get('carousel_slides')
	logging.info([carousel_slides[carousel_slide] for carousel_slide in carousel_slides])
	return [carousel_slides[carousel_slide] for carousel_slide in carousel_slides]

def get_carousel_slide(k):
	carousel_slides = memcache.get('carousel_slides')
	if not carousel_slides:
		update_carousel_slide_cache()
		carousel_slides = memcache.get('carousel_slides')
	if not k in carousel_slides:
		return None
	return carousel_slides[k]

# Users

def add_user(first_name, last_name, username, password, email):
	# check if user already exists
	if username_exists(username):
		return False

	password_hash = make_password_hash(username, password)
	now = datetime.datetime.now()

	bio = Bio(image_url='', description='')
	my_user = MyUser(datetime_created=now,
					first_name=first_name,
					last_name=last_name,
					email=email,
					username=username,
					password=password_hash,
					bio=bio,
					permissions='')

	my_user.key = my_user.put()
	cache(my_user)
	return True

def update_user_cache():
	registered_users = ndb.gql('SELECT * FROM MyUser')
	logging.info('Updated user cache.')
	d = {}
	for registered_user in registered_users:
		d[registered_user.username] = registered_user
	memcache.set('users', d)

def get_all_users(update=False):
	users = memcache.get('users')
	if update or not users:
		update_user_cache()
		users = memcache.get('users')
	return [users[user] for user in users]

def get_user(username):
	users = memcache.get('users')
	if not users:
		update_user_cache()
		users = memcache.get('users')
	if not username in users:
		return None
	return users[username]

# General caching

def cache(obj):
	if isinstance(obj, MyUser):
		d = memcache.get('users')
		d[obj.username] = obj
		memcache.set('users', d)
		logging.info("Cached a user.")
		return True

	if isinstance(obj, Article):
		d = memcache.get('articles')
		d[obj.key] = obj
		memcache.set('articles', d)
		logging.info("Cached an article.")
		return True

	return False

# Passwords and security

def make_salt(length = 5):
	return ''.join(random.choice(letters) for x in xrange(length))

def make_password_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (salt, h)

def valid_password(username, password):
	user = get_user(username)
	if not user:
		return False
	h = user.password
	salt = h.split(',')[0]
	return h == make_password_hash(username, password, salt)
