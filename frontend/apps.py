import os
from django.apps import AppConfig
from django.conf import settings


class FrontendConfig(AppConfig):
    name = 'frontend'
    app_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_webpack()

    def _set_webpack(self):
        # env = 'dev' if settings.DEGUB else 'prod'
        env = 'dev'

        settings.WEBPACK_LOADER['REPIT'] = {
            'BUNDLE_DIR_NAME': self.name + '/',
            'STATS_FILE': os.path.join(self.app_dir, 'webpack-stats.' + env + '.json'),
        }

