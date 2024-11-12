from django.apps import AppConfig


class FlexfitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flexfit'

    def ready(self):
        from .reminder import Run
        scheduler = Run()