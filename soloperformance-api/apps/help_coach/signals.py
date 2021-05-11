from  django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib import messages
from apps.help_coach import training_phase
from apps.help_coach import  models as models_help
from apps.coach import models as models_coach
import json
from django.utils.translation import ugettext as _
from webpush import send_user_notification
from webpush.utils import send_to_subscription


@receiver(post_save,sender = models_help.ProgramWorkouts)     
def send_training(sender, instance, created, *args,**kwargs):

    payload = {"head": "Welcome!", "body": "Hello World"}

   
    
    if created:
        model = models_help.ProgramWorkouts.objects.filter(pk=instance.id).first()
        program = model.program.id
        user_nivel = models_coach.NivelUser.objects.filter(user=model.program.created_by).first()
        user = model.program.created_by
        #push_infos = user.webpush_info.select_related("subscription")

      

        training = training_phase.variation_vertical_horizontal(int(program),user_nivel)    
        phse_json = json.dumps(training)   

        model.workouts_program = phse_json
        model.save()
        payload={'head': 'Solo-Performance','body': 'Your program is finished', "icon": 'https://oms-edu.org/wp-content/uploads/2019/11/solo-performance.png'}
        
        send_user_notification(user=model.program.created_by,payload=payload, ttl=1000)
        

        
        
   
    
    