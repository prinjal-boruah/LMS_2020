from callapp.models import *
import os
import requests
from django.conf import settings
import datetime

def scheduled_job():
  now=datetime.datetime.now()
  now=now+datetime.timedelta(minutes = -10)
  callrecord=Callrecords.objects.filter(record_status='No').filter(end_time__lt = now).exclude(original_record_url = -1)
  basepath="/home/sunil/callconnect/download/"
  for i in callrecord:
    r=requests.get(i.original_record_url)
    path=basepath+os.path.basename(i.original_record_url)
    with open(path,"wb") as code:
      code.write(r.content)
    pathstore="http://"+settings.HOSTNAME+"/"+"download/"+os.path.basename(i.original_record_url)
    callrecord=Callrecords.objects.get(sid=i.sid)
    callrecord.record_status='yes'
    callrecord.record_url=pathstore
    callrecord.save()
    path=''
    pathstore=''
    
    
    
