from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import re
import phonenumbers
from management.customencryption import *
from email_validator import validate_email, EmailNotValidError

class LeadStatus(models.Model):

    name =  models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    TYPE_CHOICES = (
        ('Initial', 'Initial'),
        ('Intermediate', 'Intermediate'),
        ('Finish', 'Finish'),
        ('Negative', 'Negative'),
    )

    status_type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='Initial')

    create = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class Service(models.Model):

    name = models.CharField(db_column='Service Name', max_length=100)  # Field name made lowercase.

    status = models.ManyToManyField(LeadStatus,db_column='Lead Status',blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class Package(models.Model):

    name = models.CharField(db_column='Package Name', max_length=100)  # Field name made lowercase.

    validity_days = models.IntegerField(db_column='Validity',default=365,validators=[MaxValueValidator(3000)])  # Field name made lowercase.

    lead_limit = models.BigIntegerField(db_column='Lead Limit',default=9223372036854775807)  # Field name made lowercase.

    tme_limit = models.IntegerField(db_column='TME Limit',default=0)  # Field name made lowercase.

    bd_limit = models.IntegerField(db_column='BD Limit',default=0)  # Field name made lowercase.

    tmebd_limit = models.IntegerField(db_column='TME/BD Limit',default=0)  # Field name made lowercase.

    is_livprop_tranfer = models.BooleanField(default=True,db_column='Is Fulfilment Services')

    is_encryption = models.BooleanField(default=True,db_column='Is Encryption')

    is_excel_load = models.BooleanField(default=True,db_column='Is Excel Upload')

    is_live_push_api = models.BooleanField(default=True,db_column='Is LiveChat Push API')

    is_live_pull_api = models.BooleanField(default=True,db_column='Is LiveChat Pull API')

    is_auto_assign_tme = models.BooleanField(default="False",db_column='Is Auto Assign For TME')  # Field name made lowercase.

    is_auto_assign_bd = models.BooleanField(default="False",db_column='Is Auto Assign For BD')  # Field name made lowercase.

    # is_service =  models.BooleanField(default="False",db_column='Can change Service')

    is_active = models.BooleanField(default=True,db_column='Is Active')

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class Builder(models.Model):

    id = models.CharField(primary_key=True, db_column='Builder Id',max_length=255)

    name = models.CharField(db_column='Builder Name', max_length=100)  # Field name made lowercase.


    package = models.ForeignKey(Package, on_delete=models.CASCADE,blank=True, null=True)  # Field name made lowercase.

    limit_reached = models.IntegerField(db_column='Limit Reached',default = 0)

    start_date = models.DateField(db_column='Start Date',blank=True, null=True)


    is_livprop_tranfer = models.BooleanField(default=True,db_column='Is Fulfilment Services')

    is_encryption = models.BooleanField(default=True,db_column='Is Encryption')

    is_excel_load = models.BooleanField(default=True,db_column='Is Excel Upload')

    is_live_push_api = models.BooleanField(default=True,db_column='Is LiveChat Push API')

    is_live_pull_api = models.BooleanField(default=True,db_column='Is LiveChat Pull API')

    is_auto_assign_tme = models.BooleanField(default=True,db_column='Is Auto Assign For TME')  # Field name made lowercase.

    is_auto_assign_bd = models.BooleanField(default=True,db_column='Is Auto Assign For BD')  # Field name made lowercase.


    service = models.ForeignKey(Service, on_delete=models.CASCADE,blank=True, null=True)


    is_active = models.BooleanField(default=False,db_column='Is Active')

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class UserRole(models.Model):

    name = models.CharField(db_column='Role Name', max_length=50)

    UI_TYPE_CHOICES = (
        ('MA', 'Management'),
        ('ED', 'Editing'),
    )

    ui_type = models.CharField(max_length=2,choices=UI_TYPE_CHOICES,default='MA')


    USER_TYPE_CHOICES = (
        ('FA', 'Fullfilment Admin'),
        ('SA', 'Super Admin'),
        ('FT', 'Fullfilment TME'),
        ('FB', 'Fullfilment BD'),
        ('FTB', 'Fullfilment TMEBD'),
        ('CA', 'Client Admin'),
        ('CT', 'Client TME'),
        ('CB', 'Client BD'),
        ('CTB', 'Client TMEBD'),
        ('CUS','Custome')
    )



    user_type = models.CharField(max_length=3,choices=USER_TYPE_CHOICES,default='CA')

    is_encrypted = models.BooleanField(db_column='Is Encrypted',default=True)


    # Todo add all the possible control to dynamic the role

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name




class CustomUser(AbstractUser):

    """
        by defaut from AbstractUser calls contains these fiels
        id, passowrd, is_active, date_joined, email, last_login, is_staff, last_name,
        first_name, username and is_superuser
    """
    phone = models.CharField(db_column='Phone Number',max_length=100,blank=True, null=True)

    address = models.CharField(db_column='Address', max_length=100,blank=True, null=True)

    user_roles = models.ForeignKey(UserRole,on_delete=models.CASCADE,blank=True, null=True)

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    is_login = models.BooleanField(default='True',db_column='Is Login')

    created = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.username




class Project(models.Model):

    id = models.CharField(primary_key=True, db_column='Project Id', max_length=255)

    name = models.CharField(db_column='Project Name', max_length=300)

    description = models.TextField(db_column='Project Description', blank=True, null=True)

    address = models.TextField(db_column='Project Address', blank=True, null=True)

    is_active = models.BooleanField(db_column='Is Active', default=True)

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    addresslatlong = models.CharField(db_column='Address lat long', max_length=30, blank=True, null=True)

    site_manager = models.ManyToManyField(CustomUser,db_column='Site Manager',blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    

    number = models.CharField(db_column='Phone Number',max_length=150)

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    status_error = models.TextField(max_length=200,blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # class Meta:
    #     unique_together = (('number', 'builder'),)

    def clean(self):
        if self.number and type(self.number) == str:
            #valid indian number check
            print(self.number)
            try:
                self.status_error = phonenumbers.is_valid_number(phonenumbers.parse(self.number,'IN'))
            except  Exception as e:
                self.status_error = e
            #encryption
            self.number = str_encode(self.number,True)

    def __str__(self):
        return self.number


# class PhoneNumberMany:
#     def __init__(self, numbers):
#         self.number = numbers
#         self.valid = self.split_n_frmt()


#     def split_n_frmt(self):
#         try:
#             return self.number.split(',')
#         except TypeError:
#             return []
    
#     def frmt_each(self, number):
#         if number and type(number) == str:
#             number = re.findall(r'\d+',number)[0]
#         try:
#             PhoneNumber()

#     def save_all(self):
#         all_save = 


class Emailaddress(models.Model):
    # class Meta:
    #     unique_together = (('mail_id', 'builder'),)

    mail_id = models.CharField(db_column='email',max_length=500)

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    # domain = models.CharField(max_length=100,blank=True, null=True)

    status_error = models.TextField(max_length=200,blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # class Meta:
    #     unique_together = (('mail_id', 'builder'),)

    def clean(self):
        if self.mail_id and type(self.mail_id) == str:
            try:
                v = validate_email(self.mail_id) # validate and get info
                self.mail_id  = v["email"] # replace with normalized form
            except EmailNotValidError as e:
                self.status_error = str(e)

            self.mail_id = str_encode(self.mail_id ,False)



    def __str__(self):
        return str(self.pk) + ( " : " + str(self.status_error) if self.status_error else "")



class Skype(models.Model):
    # class Meta:
    #     unique_together = (('skype_id', 'builder'),)

    skype_id = models.CharField(db_column='Skype Id',max_length=100)

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    status_error = models.TextField(max_length=200,blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.skype_id



class Country(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class City(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class SaleStatus(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name





class UnitType(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class LeadType(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class BuyingReason(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Leadsource(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


from inbound.models import *


class CallStatus(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    TYPE_CHOICES = (
        ('Initial', 'Initial'),
        ('Intermediate', 'Intermediate'),
        ('Finish', 'Finish'),
        ('Negative', 'Negative'),
    )

    status_type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='Initial')

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



from dashboard.models import *

class Lead(models.Model):

    #  comman fields from sources

    visitor_id = models.CharField(unique =True,db_column='vsid', max_length=20)

    source_date = models.DateField(db_column='Source Date',blank=True, null=True)

    name = models.CharField(db_column='Customer Name',max_length=150,blank=True, null=True)

    age = models.IntegerField(db_column='Age', blank=True, null=True,validators=[MaxValueValidator(100), MinValueValidator(18)])

    builder = models.ForeignKey(Builder, on_delete=models.CASCADE,blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)

    designation = models.CharField(db_column='Designation',max_length=65,blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    phone = models.ManyToManyField(PhoneNumber,db_column='Phone Number',blank=True)

    email = models.ManyToManyField(Emailaddress,db_column='Email',blank=True)

    skype = models.ManyToManyField(Skype,db_column='Skype',blank=True)

    country = models.ForeignKey(Country,db_column='Country', on_delete=models.CASCADE,blank=True, null=True)

    city = models.ForeignKey(City,db_column='City', on_delete=models.CASCADE,blank=True, null=True)

    live_chat = models.ManyToManyField(LiveChat,db_column='Live Chat',blank=True)


    # user need edit

    unit_type = models.ForeignKey(UnitType,db_column='Unit Type', on_delete=models.CASCADE,blank=True, null=True)

    lead_type = models.ForeignKey(LeadType,db_column='Lead Type', on_delete=models.CASCADE,blank=True, null=True)

    buying_reason = models.ForeignKey(BuyingReason,db_column='Buying Reason',on_delete=models.CASCADE,blank=True, null=True)

    from_unit_size = models.IntegerField(db_column='from Unit Size',blank=True, null=True)  # Field name made lowercase.

    to_unit_size = models.IntegerField(db_column='To Unit Size',blank=True, null=True)  # Field name made lowercase.

    from_budget = models.IntegerField(db_column='From Budget',blank=True, null=True)  # Field name made lowercase.

    to_budget = models.IntegerField(db_column='To Budget',blank=True, null=True)  # Field name made lowercase.

    additional_info = models.TextField(db_column='Additional Info',blank=True, null=True)  # Field name made lowercase.


    visit_date = models.DateField(db_column='Visit Date',blank=True, default= "1999-01-01")  # Field name made lowercase.


    lead_activity = models.ManyToManyField(LeadActivity,db_column='Lead Activity',blank=True)

    # system genrated

    address_lat_long = models.CharField(db_column='Address Lat Long', max_length=30, blank=True, null=True)

    lead_source = models.ForeignKey(Leadsource,db_column='Lead Source', on_delete=models.CASCADE,blank=True, null=True)

    # flags = models.ForeignKey(LeadFlags,db_column='Flags', on_delete=models.CASCADE,blank=True, null=True)


    tme = models.ForeignKey(CustomUser,related_name='tme',on_delete=models.CASCADE,blank=True, null=True)

    bd = models.ForeignKey(CustomUser,related_name='bd',on_delete=models.CASCADE,blank=True, null=True)

    tmebd = models.ForeignKey(CustomUser,db_column='tmebd',on_delete=models.CASCADE,blank=True, null=True)\

    last_lead_activity = models.ForeignKey(LeadActivity,on_delete=models.CASCADE,related_name='Last_Lead_Activity',blank=True, null=True)

    # last_lead_activity_call_status = models.ForeignKey(CallStatus,on_delete=models.CASCADE,blank=True, null=True)

    # last_lead_activity_lead_status = models.ForeignKey(LeadStatus,on_delete=models.CASCADE,blank=True, null=True)

    repeted_leads_info = models.ManyToManyField(APILead,db_column='APILead',blank=True)

    is_livprop_tranfer = models.BooleanField(default=True,db_column='Is Fulfilment Services')

    status_error = models.TextField(max_length=200,blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.visitor_id


class CallstatusLeadstatus(models.Model):

    service = models.ForeignKey(Service,db_column='service', on_delete=models.CASCADE,blank=True, null=True)

    call_status = models.ForeignKey(CallStatus,db_column='Call Status', on_delete=models.CASCADE,blank=True, null=True)

    lead_type = models.ManyToManyField(LeadStatus,db_column='Lead Type',blank=True)


    def __str__(self):
        return '{} - {}'.format(self.call_status, self.service)





# Log
class PrefetchUserManager(models.Manager):
    def get_queryset(self):
        return super(PrefetchUserManager, self).get_queryset().select_related('user')



class BaseRequestLog(models.Model):
    """ Logs Django rest framework API requests """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             blank=True)
    requested_at = models.DateTimeField(db_index=True)
    response_ms = models.PositiveIntegerField(default=0)
    path = models.CharField(max_length=200, db_index=True)
    view = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="From Whom"
    )

    # NOTE: Choosing the longest verb in English language - ought be good
    #       enough for a while
    VIEW_METHOD_MAX_LENGTH = len('Floccinaucinihilipilificate')
    view_method = models.CharField(
        max_length=VIEW_METHOD_MAX_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )
    remote_addr = models.GenericIPAddressField()
    host = models.URLField()
    method = models.CharField(max_length=10)
    query_params = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True,blank=True)
    objects = PrefetchUserManager()

    class Meta:
        abstract = True
        verbose_name = 'API Request Log'

    def __str__(self):
        return '{} {}'.format(self.method, self.path)




