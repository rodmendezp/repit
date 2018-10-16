from django.apps import AppConfig
from django.conf import settings


class BackendConfig(AppConfig):
    name = 'backend'
    label = 'backend'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
