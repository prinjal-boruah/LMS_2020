from django.db import models

class FielsChanged(models.Model):

    feilds = models.CharField(db_column='Source Date',max_length=30,blank=True, null=True)

    old_data = models.TextField(db_column='Old Data',blank=True, null=True)  # Field name made lowercase.

    new_data = models.TextField(db_column='New Data',blank=True, null=True)  # Field name made lowercase.

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.pk)

from management.models import LeadStatus, SaleStatus,CustomUser
from telephone.models import TelePhonekookoo
from mail.models import Email
from management.models import CallStatus

class LeadActivity(models.Model):

    Activity_Type_CHOICES = (
        ('NO', 'None'),
        ('system', 'system'),
        ('telephone_incomming', 'telephone_incomming'),
        ('telephone_outgoing', 'telephone_outgoing'),
        ('mail_outgoing', 'mail_outgoing'),
        ('cab', 'cab'),
        ('other','other')
    )

    activity_type = models.CharField(db_column='Activity Type', max_length=30, choices=Activity_Type_CHOICES,default='NO')

    telephone = models.ForeignKey(TelePhonekookoo,on_delete=models.CASCADE,blank=True, null=True)

    mail = models.ForeignKey(Email,on_delete=models.CASCADE,blank=True, null=True)

    call_status = models.ForeignKey(CallStatus,on_delete=models.CASCADE,blank=True, null=True)

    # cab = models.ForeignKey(Cab,on_delete=models.CASCADE,blank=True, null=True)


    lead_status = models.ForeignKey(LeadStatus,on_delete=models.CASCADE,blank=True, null=True)

    is_sale = models.BooleanField(db_column='Is Sale',default=False)#need to remove becouse no were used

    sale_status =  models.ForeignKey(SaleStatus,on_delete=models.CASCADE,blank=True, null=True) #need to remove becouse no were used

    next_enquiry_date = models.DateTimeField(db_column='Next Enquiry Date',blank=True, null=True)  # Field name made lowercase.

    fiels_changed = models.ManyToManyField(FielsChanged,db_column='Fiels Changed',blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='User',blank=True, null=True)

    remote_addr = models.GenericIPAddressField()

    remote_url_requested = models.URLField()

    comment =  models.TextField(blank=True, null=True)


    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.pk)
