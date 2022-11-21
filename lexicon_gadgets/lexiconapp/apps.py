from django.apps import AppConfig


class LexiconappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lexiconapp'

    def ready(self):
        import lexiconapp.signals
