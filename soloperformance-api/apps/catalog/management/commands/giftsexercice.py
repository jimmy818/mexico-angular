
from django.core.management.base import BaseCommand, CommandError
import requests
from apps.catalog import utils
from apps.catalog import models
import boto3
import botocore



                                                                                
class Command(BaseCommand):
    help = 'Add excercices'
    def handle(self, *args, **options):
        s3 = boto3.resource('s3')
        for exercice in models.Exercise.objects.all():
            for i in (number+1 for number in range(3)):
                number = i if i != 1 else ''
                try:
                    s3.Object('solo-performance-statics', "media/sp-media/GIF's/{}{}.gif".format(exercice.identifier,number)).load()
                    print('{}{}.gif already exist'.format(exercice.identifier,number))
                    path = "https://d2femlmiaazi1b.cloudfront.net/media/sp-media/GIF's/{}{}.gif".format(exercice.identifier,number)
                    file_ = models.GiftExercice.objects.filter(exercise=exercice,path=path).first()
                    if not file_:
                        item = models.GiftExercice.objects.create(
                            exercise=exercice,
                            path=path
                        )
                        item.save()

                except:
                    pass
                    # print(e)
        self.stdout.write(self.style.SUCCESS('Successfully.....'))