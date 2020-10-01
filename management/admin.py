from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(Group)
# Register your models here.

class CustomUserAdmin(UserAdmin):
    
	
	fieldsets = (
         ('basic', {
             'fields': (
                 'username', 'password', 'first_name', 'phone','address',
                 'last_name', 'email','is_active',
                 'date_joined','builder','user_roles'
                 )
                 }
         ),
        #  ("Navigation", {'fields': ('is_Encryption','is_Account', 'is_Project', 'is_Add_and_lead_enquary','is_Livprop_Tranfer','is_Auto_Tranfer','is_TME_assigin','is_BD_assigin', 'is_Livprop_status','is_TM_report','is_BD_report')}),
     )
		 
	list_display = ('username','user_roles')

    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)

    
    
    # 
        # kwargs['user_roles__user_type'] = 'CUS'
        # return 
	
	# def get_queryset(self, request):
	# 	qs = super(CustomUserAdmin, self).get_queryset(request)
	# 	if request.user.is_superuser:
	# 		qs = qs.filter(UserRole__user_type="SA") 
	# 		return qs
	# 	return qs.filter(author=request.user)

	# def has_delete_permission(self, request, obj=None):
	# 	return False

    # def def get_context_data(self, **kwargs):
    #     context = super(ViewName, self).get_context_data(**kwargs)
    #     return context

admin.site.register(CustomUser,CustomUserAdmin)




class BuilderAdmin(admin.ModelAdmin):
    pass
  
    # def has_add_permission(self, request, obj=None):
    #     return False
# 	title = 'Builder'
# 	fieldsets = [(None,{'fields': ['buildername','status']}),
# 	('Basic', {'fields': ['assignTMEtype','assignBDtype','encryption','excel','livepushAPI',]}),
# 	# ('Package',{'fields': ['packageid','startdate','expirydate']}),
# 	# ('Email Settings', {'fields': ['email_status','email_username','email_password','email_host','email_port','email_smtpsecure','email_smtpauth','email_ccaddress',]}), 
# 	# ('Phone API', {'fields': ['callConnect_status','callConnect_type','callConnect_APIstring','callParametejsonstring','callParameteoutputtype','callParametejsonoutputstring']}),
	
# 	]
# 	# class Media:
# 	# 	css = {
#     #         'all': ('/static/lms/css/admin.css',),
#     #     } 
    	
# 	# raw_id_fields = ('packageid',)


admin.site.register(Builder,BuilderAdmin)

class PackageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Package,PackageAdmin)


class UserRolesAdmin(admin.ModelAdmin):
    title = 'Role'

admin.site.register(UserRole,UserRolesAdmin)


class ServiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Service,ServiceAdmin)



class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name","builder")
    def has_add_permission(self, request, obj=None):
        return False
    

admin.site.register(Project,ProjectAdmin)


from management.mixin import APIRequestLog

class APIRequestLogAdmin(admin.ModelAdmin):
    actions = None
    date_hierarchy = 'requested_at'
   
    list_display = ('id','user', 'remote_addr', 'view', 'requested_at', 'response_ms', 'status_code',
                     'method',
                    'path',  'host'
                    )
    list_filter = ('view', 'status_code','user','requested_at')
    search_fields = ('path', 'user__email',)
    raw_id_fields = ('user', )
    list_display_links = (None)
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(APIRequestLog, APIRequestLogAdmin)



class LeadStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(LeadStatus, LeadStatusAdmin)
    

class CallstatusLeadstatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(CallstatusLeadstatus, CallstatusLeadstatusAdmin)


class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','visitor_id', 'name', 'builder', 'project', 'tme')

admin.site.register(Lead,LeadAdmin)


class EmailaddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'mail_id', 'builder' ,'status_error','created')
    
admin.site.register(Emailaddress,EmailaddressAdmin)


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'builder', 'status_error','created')
    
admin.site.register(PhoneNumber,PhoneNumberAdmin)
