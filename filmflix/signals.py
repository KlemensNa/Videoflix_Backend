from django.dispatch import receiver
from filmflix.tasks import convert_480p, convert_720p, delete_480p, delete_720p
from filmflix_backend.settings import CACHETTL
from .models import Video
from django.db.models.signals import post_save, post_delete
from django.views.decorators.cache import cache_page 
import django_rq
from django_rq import enqueue
import os

# receiver ist die funktion --> wird ausgeführt, wenn signal geschickt wird
# post_save Signal das nach dem Speichern einer Instanz gesendet wird
# sender ist das model, dass das Signal schickt
# insatnce ist entweder schon vorhanden oder wird neu erstellt
@receiver(post_save, sender=Video)
# @cache_page(CACHETTL)n

def video_post_save(sender, instance, created, **kwargs):
    print("Video wurde gespeichert")
    
    if created:
        print("New Video created")
        
        if os.path.isfile(instance.videos_file.path):
            
            # load new queue --> can also load high, low if defined
            queue = django_rq.get_queue('default', autocommit=True, is_async=True)
            
            # call function convert_xxx with in queue --> functions runs in background
            queue.enqueue(convert_480p, instance.videos_file.path)
            queue.enqueue(convert_720p, instance.videos_file.path) 


@receiver(post_delete, sender=Video)
# @cache_page(CACHETTL)
def video_post_delete(sender, instance, **kwargs):    
    
    if instance.videos_file:
        
        if os.path.isfile(instance.videos_file.path):
            
            # delete_480p(instance.videos_file.path)
            # delete_720p(instance.videos_file.path)
            os.remove(instance.videos_file.path)
            print('video gelöscht')

        
        

