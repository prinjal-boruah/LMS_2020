from django.contrib import admin
from .models import *
# Register your models here.

class PushAPIAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushAPI,PushAPIAdmin)


class PushMailAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushMail,PushMailAdmin)

class PushFlagsAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushFlags,PushFlagsAdmin)

class PushLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushLog,PushLogAdmin)