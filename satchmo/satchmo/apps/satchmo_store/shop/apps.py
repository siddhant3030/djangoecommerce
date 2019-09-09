from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'satchmo_store.shop'

    def ready(self):
        from .satchmo_settings import get_satchmo_setting
        import logging

        log = logging.getLogger('satchmo_store.shop')

        if get_satchmo_setting('MULTISHOP'):
            log.debug('patching for multishop')
            from threaded_multihost import multihost_patch

        from . import config

        from . import listeners
        listeners.start_default_listening()
