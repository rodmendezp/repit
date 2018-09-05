import six
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, PermissionsMixin, UserManager as DjangoUserManager
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        extra_fields.setdefault('is_active', True)
        return super(UserManager, self).create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        extra_fields.setdefault('is_active', True)
        return super(UserManager, self).create_superuser(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
    username = models.CharField(ugettext_lazy('username'), max_length=150, unique=True,
                                help_text='Requires 150 chars or fewer. Letters digits and @/./+/_ only.',
                                validators=[username_validator],
                                error_messages={
                                    'unique': ugettext_lazy('A user with that username already exists')
                                })
    first_name = models.CharField(ugettext_lazy('first name'), max_length=30, blank=False)
    last_name = models.CharField(ugettext_lazy('last name'), max_length=30, blank=False)
    email = models.EmailField(ugettext_lazy('email address'), unique=True, blank=False)
    is_staff = models.BooleanField(ugettext_lazy('staff status'), default=False)
    # TODO: Change is_active default to false when enable email confirmation
    is_active = models.BooleanField(ugettext_lazy('active'), default=True)
    date_joined = models.DateTimeField(ugettext_lazy('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """
    #     :param subject:
    #     :param message:
    #     :param from_email:
    #     :param kwargs:
    #     :return:
    #     """
    #     pass
    #
    # def send_activation(self, template=None, domain=None):
    #     pass

    class Meta:
        verbose_name = ugettext_lazy('user')
        verbose_name_plural = ugettext_lazy('users')




