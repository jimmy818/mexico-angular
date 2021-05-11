
from django.core.management.base import BaseCommand, CommandError
import requests
from apps.catalog import utils
from apps.catalog import models
import boto3
import botocore
import subprocess
import os


                                                                                
class Command(BaseCommand):
    help = 'Add excercices'
    def handle(self, *args, **options):
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        for exercice in models.Exercise.objects.all():
            for i in (number+1 for number in range(3)):
                number = i if i != 1 else ''
                try:
                    s3.Object('solo-performance-statics', 'media/sp-media/MP4/{}{}.mp4'.format(exercice.identifier,number)).load()
                    print('{}{}.mp4 already exist'.format(exercice.identifier,number))
                    path = 'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/MP4/{}{}.mp4'.format(exercice.identifier,number)
                    file_ = models.MediaExercice.objects.filter(exercise=exercice,path=path).first()
                    if not file_:
                        path_t = None                            
                        path_t = 'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/thumbnails/{}{}.jpg'.format(exercice.identifier,number)
                        try:
                            s3.Object('solo-performance-statics', 'media/sp-media/thumbnails/{}{}.jpg'.format(exercice.identifier,number).format(exercice.identifier,number)).load()
                        except:
                            s3_client.download_file('solo-performance-statics', 'media/sp-media/MP4/{}{}.mp4'.format(exercice.identifier,number), '/tmp/{}{}.mp4'.format(exercice.identifier,number))
                            thumbnail = generate_thumbnail('/tmp/{}{}.mp4'.format(exercice.identifier,number),'/tmp/{}{}.jpg'.format(exercice.identifier,number))
                            if thumbnail['success']:
                                s3.meta.client.upload_file(thumbnail['message'], 'solo-performance-statics', 'media/sp-media/thumbnails/{}{}.jpg'.format(exercice.identifier,number))
                                os.remove(thumbnail['message'])
                                os.remove('/tmp/{}{}.mp4'.format(exercice.identifier,number))
                        item = models.MediaExercice.objects.create(
                            exercise=exercice,
                            path=path,
                            thumbnail=path_t
                        )
                        item.save()

                except Exception as e:
                    pass
                    # print(e)
        self.stdout.write(self.style.SUCCESS('Successfully.....'))


def generate_thumbnail(path,image_path):
    try:
        # ffmpeg -i "/tmp/Carioca.mp4" -ss 1 -vframes 1 "image.jpg"
        subprocess.call(['ffmpeg', '-i', path, '-ss', '0.0' ,'-vframes', '1','-s','960x540', image_path])
        return {
            "success":True,
            "message": image_path
        }
    except Exception as e:
        return {
            "success":False,
            "message": e
        }
