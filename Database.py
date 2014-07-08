from Handler import *
from google.appengine.ext import ndb
from google.appengine.api import memcache
import hashlib
import random
from string import letters
import datetime

users_key = "users"

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
	bio_is_displayed = ndb.BooleanProperty(required=True)

	is_a_moderator = ndb.BooleanProperty(required=True)

	can_create_news_posts = ndb.BooleanProperty(required=True)
	can_edit_news_posts = ndb.BooleanProperty(required=True)

	can_claim_workshops = ndb.BooleanProperty(required=True)
	can_free_workshops = ndb.BooleanProperty(required=True)

	can_edit_homepage = ndb.BooleanProperty(required=True)


def add_user(first_name, last_name, username, password, email):
	# check if user already exists
	if username_exists(username):
		return False

	password_hash = make_password_hash(username, password)
	now = datetime.datetime.now()

	bio = Bio(image_url='', description='')
	my_user = MyUser(first_name=first_name,
					last_name=last_name,
					email=email,
					username=username,
					password=password_hash,
					bio=bio,
					bio_is_displayed=False,
					is_a_moderator=False,
					can_create_news_posts=False,
					can_edit_news_posts=False,
					can_claim_workshops=False,
					can_free_workshops=False,
					can_edit_homepage=False)

	my_user.put()
	# update memcache
	my_users = memcache.get(users_key)
	add_user_to_dict(my_user, my_users)
	memcache.set(users_key, my_users)
	return True

def username_exists(username):
	return username in get_all_users()

def is_registered_user(user, update=False):
	if not user:
		return False
	return username_exists(user.username())

def get_all_users(update=False):
	my_users = memcache.get(users_key)

	# update
	if my_users is None or update:
		update_user_memcache()
		my_users = memcache.get(users_key)

	return my_users

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
	user_exists = user.user_id() in get_all_users()
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
	h = user.password_hash
	salt = h.split(',')[0]
	return h == make_password_hash(username, password, salt)
