from Handler import *
from google.appengine.ext import ndb
from google.appengine.api import memcache
import hashlib
import random
from string import letters
import datetime

users_key = 'users'
slides_key = 'slides'
shows_key = 'shows'

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
	datetime_created = ndb.DateTimeProperty(auto_now_add=True)

	image_url = ndb.StringProperty(required=True)

	title = ndb.StringProperty()
	description = ndb.StringProperty()

	button_text = ndb.StringProperty()
	button_link = ndb.StringProperty()


class Show(ndb.Model):
	slide = ndb.StructuredProperty(CarouselSlide)

	max_reservations = ndb.IntegerProperty()
	num_reservations = ndb.IntegerProperty()

class Article(ndb.Model):
	heading = ndb.StringProperty()
	summary = ndb.TextProperty()
	content = ndb.TextProperty()

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

	my_user.put()
	# update memcache
	my_users = memcache.get(users_key)
	add_user_to_dict(my_user, my_users)
	memcache.set(users_key, my_users)
	return True


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
	my_users = memcache.get(users_key)
	add_user_to_dict(my_user, my_users)
	memcache.set(users_key, my_users)
	return True

def has_permission(username, s):
	my_user = get_user(username)
	if not my_user:
		return False
	return s in my_user.permissions

def username_exists(username):
	return username in get_user_dict()

def is_registered_user(user, update=False):
	if not user:
		return False
	return username_exists(user.username())

def get_user(username):
	if not username in get_user_dict():
		return None
	return get_user_dict()[username]

def get_user_dict(update=False):
	my_users = memcache.get(users_key)

	# update
	if my_users is None or update:
		update_user_memcache()
		my_users = memcache.get(users_key)

	return my_users

def get_all_users(update=False):
	users = get_user_dict(update)
	return [users[user] for user in users]

def update_user_memcache():
	registered_users = ndb.gql("SELECT * FROM MyUser")
	my_user_dict = {}
	for registered_user in registered_users:
		add_user_to_dict(registered_user, my_user_dict)
	memcache.set(users_key, my_user_dict)

def add_user_to_dict(my_user, d):
	d[my_user.username] = my_user

def is_registered_user(user, update=False):
	if not user:
		return False

	# check if user exists
	user_exists = user.user_id() in get_user_dict()
	return user_exists

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
