from django.db import models

from management.models import *


'''
Todo list
#/    ServerId (table create)
#/    WebSiteUrl (table create)
#/    Folder (table create)
#/    Source (table create)


'''


'''
/compid=14475                                                                builder.id
#visemail=Nill                                                               email  (M , ',')
#visphone=9410078375, 9675017712                                             phone  (M , ',')
/leadDate=2018-01-24                                                         lead_date
/customerName=Viny                                                           name
/country=India                                                               country
/city=Karimnagar                                                             city
/propid=17059                                                                project.id
/property=Enquiry[Park West (Apts) - Bangalore]                              project.name
/chat=1128218012412301301                                                    visitor_id
/cmpname=Shapoorji Pallonji Real Estate                                      builder.name
source = "google.com"
fldrname=B1-C1282                                                            BuilderChatInfo.folder
serverid=ms1.livserv.in                                                      server_id
websiteurl=http://shapoorjirealestate.com/parkwest/                          web_site_url

reference URL
UTM source
UTM compain 
sid
Home URL
extra Two unnamed parameters 

'''


class APILead(models.Model):
    chVisitid = models.CharField(max_length=200)
    compid = models.CharField(max_length=200)
    visemail = models.CharField(max_length=200,blank=True, null=True)                                                            
    visphone = models.CharField(max_length=200,blank=True, null=True)
    leadDate = models.CharField(max_length=200,blank=True, null=True)
    customerName = models.CharField(max_length=200,blank=True, null=True)
    country = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    propid = models.CharField(max_length=200)
    property = models.CharField(max_length=200)
    cmpname = models.CharField(max_length=200)
    fldrname = models.CharField(max_length=200,blank=True, null=True)
    serverid = models.CharField(max_length=200,blank=True, null=True)
    websiteurl = models.CharField(max_length=200,blank=True, null=True)
    source = models.CharField(max_length=200,blank=True, null=True)
    additional = models.CharField(max_length=200,blank=True, null=True)
    flag = models.BooleanField(default=True)
    status_error = models.TextField(max_length=200,blank=True, null=True)

    def __str__(self):
        return str(self.chVisitid)






class ServerId(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name



class WebSiteUrl(models.Model):

    name = models.CharField(db_column='name',max_length=250)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

        


class Folder(models.Model):

    name = models.CharField(db_column='name',max_length=100)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name


class Source(models.Model):

    name = models.CharField(db_column='name',max_length=250)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

        

class LiveChat(models.Model):

    web_site_url =  models.ForeignKey(WebSiteUrl,db_column='WebSiteUrl', on_delete=models.CASCADE,blank=True, null=True)

    source = models.ForeignKey(Source,db_column='Source', on_delete=models.CASCADE,blank=True, null=True)

    folder = models.ForeignKey(Folder,db_column='Folder', on_delete=models.CASCADE,blank=True, null=True)

    server_id = models.ForeignKey(ServerId,db_column='ServerId', on_delete=models.CASCADE,blank=True, null=True)
 
    additional = models.TextField(db_column='Additional', blank=True, null=True)

    chat_url = models.URLField(blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return str(self.pk)

# auto assigin related tables 
class AgentAvailability(models.Model):

    agent = models.ForeignKey(CustomUser,related_name='agent',on_delete=models.CASCADE)

    from_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    to_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    who_updated = models.ForeignKey(CustomUser,related_name='who_updated',on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class LeadAssignPriority(models.Model):

    agent = models.ForeignKey(CustomUser,related_name='agentL',on_delete=models.CASCADE)
    
    from_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    to_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    projects = models.ManyToManyField(Project,db_column='Fiels Changed',blank=True)

    who_updated = models.ForeignKey(CustomUser,related_name='who_updatedL',on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.pk)
 
    




class BuilderAutoAssignInfo(models.Model):

    builder = models.OneToOneField(Builder,on_delete=models.CASCADE,primary_key=True) 

    last_tme = models.ForeignKey(CustomUser,related_name='lasttme',on_delete=models.CASCADE,null=True,blank=True)

    last_bd = models.ForeignKey(CustomUser,related_name='lastbd',on_delete=models.CASCADE,null=True,blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.builder.name)

