import os

ADMIN_ENABLED = True

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-5owfq%%7(d!)+6^sxc+g637hh9+obhk4fj8_(a5e)3ngir8v^+')

DATABASES = {
    'host': os.environ.get('DATABASE_HOST', ''),
    'user': os.environ.get('DATABASE_USER', ''),
    'pass': os.environ.get('DATABASE_PASS', ''),
    'name': os.environ.get('DATABASE_NAME', '')
}

HASHIDS_SALT = {
    'user_id': 'HzN8V2zfccyTcAAL',
    'undangan_id': 'RchKkW2Rm798kqyq',
    'ucapan_id': '5ApYwHieqQRB0ccF'
}

ALLOWED_HOSTS = []

app_config = {
    'secret_key': SECRET_KEY,
    'db_host': DATABASES.get('host'),
    'db_user': DATABASES.get('user'),
    'db_pass': DATABASES.get('pass'),
    'db_name': DATABASES.get('name'),
    'salt_user': HASHIDS_SALT.get('user_id'),
    'salt_undangan': HASHIDS_SALT.get('undangan'),
    'salt_ucapan': HASHIDS_SALT.get('ucapan'),
    'allowed_hosts': ALLOWED_HOSTS,
    'admin_enabled': ADMIN_ENABLED,
    'is_debug': DEBUG,
}