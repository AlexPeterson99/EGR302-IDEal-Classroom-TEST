from django.apps import AppConfig


class IdealClassroomConfig(AppConfig):
    name = 'ideal_classroom'

    # ready method overwritten by Abanoub Farag on 4/14/2020 to start scheduled tasks on launch of server
    def ready(self):
        from .tasks import start
        start()