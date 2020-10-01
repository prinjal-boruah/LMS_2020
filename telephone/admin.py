from django.contrib import admin
from .models import *
# Register your models here.

class BuilderCallInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(BuilderCallInfo, BuilderCallInfoAdmin)



class BuilderCallInfoKookooAdmin(admin.ModelAdmin):
    pass

admin.site.register(BuilderCallInfoKookoo, BuilderCallInfoKookooAdmin)