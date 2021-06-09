from django.apps import AppConfig


class BaseappConfig(AppConfig):
    name = 'BaseApp'

    def ready(self) -> None:
        from scheduler import updater
        updater.start()
