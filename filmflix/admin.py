
from django.contrib import admin
from .models import Video, CustomerUser
from django.contrib.auth.admin import UserAdmin
# import CustomerUser (register app in settings and set AUTH_USER_MODEL to path of own model)
# import UserAdmin to fix style of Userinterface to default style
admin.site.register(Video)
admin.site.register(CustomerUser, UserAdmin)