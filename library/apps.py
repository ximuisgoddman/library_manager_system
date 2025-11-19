from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        # Lazily attempt the captcha compatibility patch once Django is fully
        # initialised (settings configured, INSTALLED_APPS loaded).
        from . import captcha_compat

        captcha_compat.patch_captcha_getsize()

