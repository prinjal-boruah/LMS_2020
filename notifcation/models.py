from django.db import models

# Create your models here.\
from management.models import CustomUser,Lead

# class Notifcation(models.Model):

#     CustomUserid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     leadnumber = models.ForeignKey(Lead, on_delete=models.CASCADE) 

#     issitevisit =  models.BooleanField(default="False")

#     read = models.BooleanField(default="False")




class Notifcation(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    data = models.TextField(null=True, blank=True)

    # status =  models.BooleanField(default="True")

    # read = models.BooleanField(default="False")




# class CallNotifcation(models.Model):

#     leadnumber = models.ForeignKey(Lead, on_delete=models.CASCADE) 

#     data = models.CharField(db_column='data',max_length=150,blank=True, null=True) 



# class IncommingCall(models.Model):

#     CustomUserid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     leadnumber = models.ForeignKey(Lead, on_delete=models.CASCADE) 

#     leadname = models.CharField(db_column='leadname',max_length=150,blank=True, null=True) 

#     call_status = models.CharField(db_column='data',max_length=150,blank=True, null=True) 

#     created = models.DateTimeField(auto_now=False, auto_now_add=True)




