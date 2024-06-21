from django.apps import AppConfig


class OcservConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ocserv'

    def ready(self):
        import ocserv.signals
