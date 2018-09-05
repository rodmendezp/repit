from django.apps import AppConfig
from django.conf import settings


class BackendConfig(AppConfig):
    name = 'backend'
    label = 'backend'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_subdomain()

    def _set_subdomain(self):
        # settings.SUBDOMAIN_URLCONFS['kabara'] = self.name + '.urls'
        pass
