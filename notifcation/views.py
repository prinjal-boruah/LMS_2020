from notifcation.models import *
from management.models import *
from django.http import HttpResponse, JsonResponse
from django.views import View

from django.db.models import Q
import datetime

from django.db.models import Max

# telephonekookoo.status 
class CallNotifcationView(View):
    def get(self,request):
        telePhonekookoo = TelePhonekookoo.objects.get(sid=request.GET['sid'])  
        return HttpResponse(telePhonekookoo.status)
        

class InfoNotifcationView(View):
    def get(self,request):
        user = CustomUser.objects.get(pk = request.session['userid'])
        query = Q()
        queryT = Lead.objects.filter( tme = user)
        aat = queryT.count()
        aac = queryT.filter(last_lead_activity__lead_status__status_type = "Finish").count()   
        aaf = queryT.filter(last_lead_activity__lead_status__status_type = "Intermediate").count()  
        
        today = datetime.date.today()

        queryM = queryT.filter(source_date__month = today.month).filter(source_date__year = today.year)      
        mmt = queryM.count()
        mmc = queryM.filter(last_lead_activity__lead_status__status_type = "Finish").count()   
        mmf = queryM.filter(last_lead_activity__lead_status__status_type = "Intermediate").count() 
    

        start_week = today - datetime.timedelta(today.weekday())
        end_week = start_week + datetime.timedelta(7)
        queryW = queryM.filter(source_date__range=[start_week, end_week])        
        wwt = queryW.count()
        wwc = queryW.filter(last_lead_activity__lead_status__status_type = "Finish").count()   
        wwf = queryW.filter(last_lead_activity__lead_status__status_type = "Intermediate").count()

        queryD = queryW.filter(source_date__day=today.day)        
        ddt = queryD.count()
        ddc = queryD.filter(last_lead_activity__lead_status__status_type = "Finish").count()   
        ddf = queryD.filter(last_lead_activity__lead_status__status_type = "Intermediate").count()


  
        context = {
            'ddf' : ddf, 'ddc' : ddc, 'ddt' : ddt, 'wwf' : wwf,'wwc' : wwc, 'wwt' : wwt, 'mmf' : mmf,
            'mmc' : mmc, 'mmt' : mmt, 'aaf' : aaf, 'aac' : aac, 'aat' : aat, 'datetimeofinfo':datetime.datetime.today().strftime("%Y-%m-%d %H:%M %p")
        }
        
        return JsonResponse(context)
       




class NotifcationView(View):
    def get(self,request):
        user = CustomUser.objects.get(pk = request.session['userid'])
        query = Q()
        queryT = Lead.objects.filter( tme = user)
        newLeads = queryT.filter(last_lead_activity__lead_status__status_type = "Initial").count()   
        context = {
            'newLeads' : newLeads,  'newLeadsdatetimeofinfo':datetime.datetime.today().strftime("%Y-%m-%d %H:%M %p")
        }
        
        return JsonResponse(context)



class AlertNotifcationView(View):
    def get(self,request):
        query = Lead.objects.filter(
            tme = CustomUser.objects.get(pk = request.session['userid'])).filter(
            last_lead_activity__next_enquiry_date__range = (
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(days=1))
            )
         
        alertLeads = []

        for each in query:
            alertLeads.append(
                {
                    "name":each.name,
                    'leadid' :each.id,
                    "name":each.name,
                    "status":each.last_lead_activity.lead_status.name,
                    "time":  (each.last_lead_activity.next_enquiry_date + datetime.timedelta(hours=5,minutes=30)).strftime('%I:%M %p'),
                    "datetime":datetime.datetime.today().strftime("%Y-%m-%d %H:%M %p")
                }
            )
       
        context = {
            'alertLeads' : alertLeads,
            'count':len(alertLeads)
        }
        
        return JsonResponse(context)



class IncomingalertView(View):
    def get(self,request):
        lead = Lead.objects.annotate(Max('lead_activity__id')).filter(lead_activity__activity_type="telephone_incomming")
        listsids = []
        for each in lead:
            if each.lead_activity.last().activity_type == "telephone_incomming":
                listsid = {
                    'leadid' :each.id,
                    'name':each.name,
                    'datetime':each.modified,
                    'sid':each.lead_activity.last().sid,
                    'leadstatus':"lead.lead_activity.last().lead_status.name",
                    'callstatus':each.lead_activity.last().status.replace('Agent','')
                }
                listsids.append(listsid)

        
        context = {
            'count' : len(listsids),
            "listofsid" : listsids
        }
        
        return JsonResponse(context)
