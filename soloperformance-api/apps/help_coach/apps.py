from django.apps import AppConfig
from django.db.models.signals import post_save

class HelpCoachConfig(AppConfig):
    name = 'help_coach'
    
    
    
    def ready(self):
        from .models import  ProgramWorkouts

        from apps.help_coach.signals import send_training # noqa
        post_save.connect(send_training, dender = ProgramWorkouts)
