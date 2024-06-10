from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Video, CustomerUser
from django.contrib.auth.admin import UserAdmin



# import CustomerUser (register app in settings and set AUTH_USER_MODEL to path of own model)
# import UserAdmin to fix style of Userinterface to default style


# script zum exportieren und importieren schreiben
# importExport --> nochmal anschauen, weil Video keine Erklärung liefert
class VideoResource(resources.ModelResource):

    class Meta:
        model = Video  
        
        
@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    pass

admin.site.register(CustomerUser, UserAdmin)