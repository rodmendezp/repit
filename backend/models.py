import six
import sendgrid
from sendgrid.helpers.mail.email import Email
from sendgrid.helpers.mail.content import Content
from sendgrid.helpers.mail.mail import Mail
from .tokens import account_activation_token
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, PermissionsMixin, UserManager as DjangoUserManager
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser
from Repit.settings import SENDGRID_API_KEY, ADMIN_EMAIL


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
    is_active = models.BooleanField(ugettext_lazy('active'), default=False)
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

    def email_user(self, subject, message, from_email=None, **kwargs):
        to_email = kwargs['to_email'] if 'to_email' in kwargs else self.email
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email(from_email)
        to_email = Email(to_email)
        content_type = kwargs['content_type'] if 'content_type' in kwargs else 'text/plain'
        content = Content(  content_type, message)
        email = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=email.get())
        return response

    def send_activation(self, template=None, domain=None):
        self.email_template = template or 'emails/registration/activate.html'
        domain = domain or Site.objects.get_current().domain
        self.email_params = {
            'user': self,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)).decode("utf-8"),
            'token': account_activation_token.make_token(self),
        }
        message = render_to_string(self.email_template, self.email_params)
        self.email_response = self.email_user(
            'Welcome To Repit',
            message,
            ADMIN_EMAIL,
            content_type='text/html'
        )
        return self.email_response, self.email_template, self.email_params

    class Meta:
        verbose_name = ugettext_lazy('user')
        verbose_name_plural = ugettext_lazy('users')




