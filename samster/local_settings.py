# Django local_settings for samster project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PRODUCTION_READY = not DEBUG

ADMINS = (
    ('First Last', 'no@reply.com'),
)

MANAGERS = ADMINS

CONTACT_EMAIL_RECIPIENT = ["no@reply.com"]
DEFAULT_FROM_EMAIL = 'no@reply.com'
SITENAME = "sitename.com"
PROPER_NAME = "Proper Name"
EMPTY_TEXT = "The text displayed for pages with no text"


# For 'The River' Page --------------------------------

TWITTER = {
    'CONSUMER_KEY': '',
    'CONSUMER_SECRET': '',
    'ACCESS_TOKEN_KEY': '',
    'ACCESS_TOKEN_SECRET': ''
}

SOUNDCLOUD = {
    'CLIENT_ID': '',
    'USER_ID': ''
}

LASTFM = {
    'KEY': '',
    'SECRET': '',
    'USERNAME': ''
}

FLICKR = {
    'KEY': '',
    'SECRET': '',
    'USER_ID': '',
    'USERNAME': ''
}

LINKEDIN = {
    'USERNAME': ''
}

GITHUB = {
    'USERNAME': ''
}

IMGUR = {
    'CLIENT_ID': '',
    'SECRET': '',
    'ACCESS_CODE': '',
    'USERNAME': ''
}

FACEBOOK = {}  # Abandoning. Too hard. I don't know how. Facebook sucks.

# -----------------------------------------------------


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
