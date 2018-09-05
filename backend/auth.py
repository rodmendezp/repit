from ratelimitbackend.backends import RateLimitModelBackend
from ratelimitbackend.exceptions import RateLimitException
from django.contrib.auth import get_user_model


class CustomRateLimitModelBackend(RateLimitModelBackend):
    def get_ip(self, request):
        if 'REMOTE_ADDR' in request.META:
            return request.META['REMOTE_ADDR']
        elif 'HTTP_REMOTE_ADDR' in request.META:
            return request.META['HTTP_REMOTE_ADDR']
        elif 'HTTP_X_REAL_IP' in request.META:
            return request.META['HTTP_X_REAL_IP']
        return '1.1.1.1'


class EmailBackend(CustomRateLimitModelBackend):
    cache_prefix = 'rlebackend-'
    # At most 15 login attempts in 60 minutes
    minutes = 60
    requests = 300

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        if request is not None:
            counts = self.get_counters(request)
            if sum(counts.values()) >= self.requests:
                raise RateLimitException('Rate-limit reached', counts)

        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            user = None

        if user and not user.check_password(password) or not self.user_can_authenticate(user):
            user = None

        if user is None and request is not None:
            cache_key = self.get_cache_key(request)
            self.cache_incr(cache_key)

        return user
