from django.contrib import admin
from .models import *
# Register your models here.

class AgentAvailabilityAdmin(admin.ModelAdmin):
    pass

admin.site.register(AgentAvailability,AgentAvailabilityAdmin)



class LeadAssignPriorityAdmin(admin.ModelAdmin):
    list_display = ("agent","from_date","to_date")

admin.site.register(LeadAssignPriority,LeadAssignPriorityAdmin)


class APILeadAdmin(admin.ModelAdmin):
    list_display = ("chVisitid","customerName","cmpname","property","leadDate")
    pass

admin.site.register(APILead,APILeadAdmin)


