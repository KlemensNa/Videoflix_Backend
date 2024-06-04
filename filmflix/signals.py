from django.dispatch import receiver
from filmflix.tasks import convert_480p, convert_720p, delete_480p, delete_720p
from .models import Video
from django.db.models.signals import post_save, post_delete
import os

# receiver ist die funktion --> wird ausgeführt, wenn signal geschickt wird
# post_save Signal das nach dem Speichern einer Instanz gesendet wird
# sender ist das model, dass das Signal schickt
# insatnce ist entweder schon vorhanden oder wird neu erstellt
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video wurde gespeichert")
    print(instance.videos_file.path)
    #wird nur ausgeführt wenn wirklich neue Instanz erstellt wurde
    if created:
        print("New Video created")
        if os.path.isfile(instance.videos_file.path):     
            convert_480p(instance.videos_file.path)
            convert_720p(instance.videos_file.path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):    
    
    if instance.videos_file:
        
        if os.path.isfile(instance.videos_file.path):
            os.remove(instance.videos_file.path)
            delete_480p(instance.videos_file.path)
            delete_720p(instance.videos_file.path)
            print('video gelöscht')

        
        

