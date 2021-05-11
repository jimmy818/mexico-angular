from apps.catalog import models
import boto3
import subprocess
import tempfile, shutil, os   

# VALIDATE IN S3 IF EXIST NAME FILE TO LOAD
def validate_file_s3(name):
    s3 = boto3.resource('s3')
    try:
        s3.Object('solo-performance-statics', 'media/sp-media/MP4/{}'.format(name)).load()
        path_video = 'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/MP4/{}'.format(name)
        path_image = 'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/thumbnails/{}.jpg'.format(name.split('.')[0])

        return {
            'video':path_video,
            'img':path_image
        }

       
    except Exception as e:
        return None
        # print(e)

def upload_file(file,name):
    s3 = boto3.resource('s3')
    outfile = tempfile.NamedTemporaryFile(suffix=".mp4")  
    outfile.write(file.read())
    print(outfile.name)
    thumbnail = generate_thumbnail(outfile.name,'/tmp/{}.jpg'.format(name.split('.')[0]))
    if thumbnail['success']:
        s3.meta.client.upload_file(thumbnail['message'], 'solo-performance-statics', 'media/sp-media/thumbnails/{}.jpg'.format(name.split('.')[0]))
        s3.meta.client.upload_file(outfile.name, 'solo-performance-statics', 'media/sp-media/MP4/{}'.format(name))
        os.remove(thumbnail['message'])
    outfile.close()

    return {
        'video':'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/MP4/{}'.format(name),
        'img':'https://d2femlmiaazi1b.cloudfront.net/media/sp-media/thumbnails/{}.jpg'.format(name.split('.')[0])
    }




def generate_thumbnail(path,image_path):
    try:
        # ffmpeg -i "/tmp/Carioca.mp4" -ss 1 -vframes 1 "image.jpg"
        subprocess.call(['ffmpeg', '-y','-i', path, '-ss', '0.0' ,'-vframes', '1','-s','960x540', image_path])
        return {
            "success":True,
            "message": image_path
        }
    except Exception as e:
        return {
            "success":False,
            "message": e
        }
#  try:
#             s3.Object('solo-performance-statics', 'media/sp-media/thumbnails/{}{}.jpg'.format(exercice.identifier,number).format(exercice.identifier,number)).load()
#         except:
#             s3_client.download_file('solo-performance-statics', 'media/sp-media/MP4/{}{}.mp4'.format(exercice.identifier,number), '/tmp/{}{}.mp4'.format(exercice.identifier,number))
#             thumbnail = generate_thumbnail('/tmp/{}{}.mp4'.format(exercice.identifier,number),'/tmp/{}{}.jpg'.format(exercice.identifier,number))
#             if thumbnail['success']:
#                 s3.meta.client.upload_file(thumbnail['message'], 'solo-performance-statics', 'media/sp-media/thumbnails/{}{}.jpg'.format(exercice.identifier,number))
#                 os.remove(thumbnail['message'])
#                 os.remove('/tmp/{}{}.mp4'.format(exercice.identifier,number))
#         item = models.MediaExercice.objects.create(
#             exercise=exercice,
#             path=path,
#             thumbnail=path_t
#         )
#         item.save()