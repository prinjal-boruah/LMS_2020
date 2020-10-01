# from telephone.models import *
# import requests;
# import xml.etree.cElementTree as ET
# from  telephone.kookoo import *
# from django.http import HttpResponse
# from django.contrib.sites.shortcuts import get_current_site


# def callDataInsert(sid,data):
#   pass
#   # callrecord=Callrecords.objects.get(sid=sid)
#   # callrecord.caller_id=data['caller_id']
#   # callrecord.phone_no=data['phone_no']
#   # callrecord.duration=data['duration']
#   # callrecord.start_time=data['start_time']
#   # callrecord.agent_status=data['status']
#   # callrecord.status_details=data['status_details']
#   # callrecord.record_status='No'
#   # callrecord.ringing_time=data['ringing_time']
#   # callrecord.dial_time=data['dial_time']
#   # callrecord.pick_time=data['pick_time']
#   # callrecord.end_time=data['end_time']
#   # callrecord.save()

# def callUrl(agent,callback_url,cid,request):
#   r = Response()
#   url = 'http://www.kookoo.in/outbound/outbound.php'
#   params = {'api_key': 'KKe29511dd73f0e516f69636720ff297b2',
#            'phone_no' : agent,
#            'caller_id' : '918067947251',
#            'outbound_version' : 2,
#            'url':''.join(['http://', get_current_site(request).domain,'/telephone/calldial/?mcid=',cid]),
#            'callback_url':callback_url,
#          }
#   r1 = requests.get(url, params=params)
#   #r.addDial('9535629202',record='true',limittime="1000",timeout="30",moh='default',\promptToCalledNumber='no',caller_id='918067947251')
  
#   return r;
# def inboundUrl(agent,callback_url):
#   url = 'http://www.kookoo.in/outbound/outbound.php'
#   params = {'api_key': 'KKe29511dd73f0e516f69636720ff297b2',
#            'phone_no' : '9535629202',
#            'caller_id' : '918067947251',
#            #'outbound_version' : 2,
#            #'url':'http://106.51.37.192:8020/click2call_testing/dial.php?dial_to=9880486655',
#            'url':'http://106.51.37.192:8013/calldial',
#            #'extra_data': '<response><dial>7829511581</dial></response>',
#            'callback_url':callback_url,
#            }
#   r = requests.get(url, params=params)
#   return r;
# """
# def addDial(dial):
#   doc = ET.Element("response")
#   ET.SubElement(doc, "dial").text = dial
#   ET.ElementTree(doc)
# """

