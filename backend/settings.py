from Repit.settings import AUTHENTICATION_BACKENDS


AUTHENTICATION_BACKENDS.append('backend.auth.EmailBackend')
AUTH_USER_MODEL = 'backend.User'