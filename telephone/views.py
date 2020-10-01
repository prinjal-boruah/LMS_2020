from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site

from management.models import * 
from .models import *

from .kookoo import *

import requests
import xml.etree.ElementTree as ET
import datetime
import base64
import json
import phonenumbers
from django.db.models import Q
from notifcation.models import *

@csrf_exempt
def callConnect(request):
  
  leadid = request.POST.get('leadid')
  phoneid = request.POST.get('phoneid')
  # fetching Lead 
  print(phoneid)
  lead = Lead.objects.get(id=leadid)
  # fetching builder 
  builder = BuilderCallInfo.objects.filter(builder = lead.builder.id)
  # activate creating
  lead_activity1 = LeadActivity(
            activity_type = 'telephone_outgoing',
            remote_addr = request.META['REMOTE_ADDR'],
            remote_url_requested = request.META['HTTP_REFERER'],
  )
  lead_activity1.user = CustomUser.objects.get(pk = request.session['userid'])
  lead_activity1.save()

  lead.lead_activity.add(lead_activity1)

  # time restrict 

  NowT = datetime.datetime.now().hour
  print(NowT)
  if NowT < 9 and NowT > 18:
    lead_activity1.comment = "LMSstatus:11"
    lead_activity1.save()
    return JsonResponse({
        "LMSstatus":11,
        "additional":"Calling Time is Over. try in between 9AM to 6PM (error code:TRAI Guidance)"
    })



  # validation
  if len(builder) == 0:
    lead_activity1.comment = "LMSstatus:10"
    lead_activity1.save()
    return JsonResponse({
        "LMSstatus":10,
        "additional":"Calling is not activated please inform Admin  (error code:builder_call_info)"
    })
  else:
    builder = builder[0]


  # muiltiple connection 
  if builder.type_of_connection == 'KooKoo':
    # kookoo
    
    # kookoo validation
    if builder.builder_call_info_kookoo == None:
      lead_activity1.comment = "LMSstatus:9"
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":9,
        "additional":"Calling is not activated please inform Admin (error code:builder_call_info_kookoo)"
      })
    
    # agent Validation
    if lead.tme.phone == None:
      lead_activity1.comment = "LMSstatus:8"
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":8,
        "additional":"Please provide agent number"
      })
      

    # phone validation
    number=phonenumbers.parse(lead.tme.phone,'IN')
    if phonenumbers.is_valid_number(number) == False:
      lead_activity1.comment = "LMSstatus:7"
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":7,
        "additional":"Please provide valid agent number"
      })
    # import pdb; pdb.set_trace()
    visitornu = str_decode(PhoneNumber.objects.get(pk = phoneid).number)
    number=phonenumbers.parse(visitornu,'IN')
    if phonenumbers.is_valid_number(number) == False:
      lead_activity1.comment = "LMSstatus:6"
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":6,
        "additional":"Invalid Visitor number"
      })
    
    # need to check interntional 

    builder_kookoo = builder.builder_call_info_kookoo
    
    params_data =  {
                    'api_key': builder_kookoo.api_key, 
                    'phone_no' : lead.tme.phone, # agent number
                    'caller_id' : builder_kookoo.caller_id , # did
                    'outbound_version' : 2,
                    'url': ''.join(['http://', get_current_site(request).domain,'/telephone/kookoo/calldial/?mcid=',leadid]) # callback URL
            } 

    url = 'http://www.kookoo.in/outbound/outbound.php/'
    print(params_data)

    # datetime or request
    datetime_of_request = datetime.datetime.now()
    
    #request
    r_data = requests.get(url,params = params_data)
    root =  ET.fromstring(r_data.text)
    print(r_data.text)

    if root.getchildren()[1].text == "Authentication error":
      lead_activity1.comment = "LMSstatus:12"
      lead_activity1.save()
      return JsonResponse({
          "LMSstatus":12,
          "additional":"Kookoo Authentication error"
      })


    #request datatable
    telePhonekookoo1 = TelePhonekookoo.objects.create(
      sid = root.getchildren()[1].text,
      user = CustomUser.objects.get(id=request.session['userid']),
      lead = lead.id,
      phone = PhoneNumber.objects.get(pk = phoneid),
      status = "ConnectingAgent",
      call_type = "Out"
    )
    print("Call ********** ConnectingAgent *********")
    #log
    RequestLog.objects.create(
      requested_at = datetime_of_request,
      response_ms = r_data.elapsed.total_seconds(),
      # requested_params = base64.b64encode(json.dumps(params_data).encode()),
      requested_params = json.dumps(params_data), # need to remve this in Production
      requested_status_code = r_data.status_code,
      requested_method = r_data.request.method,
      requested_response = r_data.text,
      requested_errors = "",
      requested_url = url,
      # application specific 
      user_remote_addr = request.META['REMOTE_ADDR'],
      user_host =  get_current_site(request).domain + request.path_info,
      user = CustomUser.objects.get(id=request.session['userid']),
      response_sid = root.getchildren()[1].text,
    )

    #succesful with sid 
    if len(root.getchildren()) > 0:
      lead_activity1.telephone = telePhonekookoo1
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":1,
        "additional":"Connecting.. through KooKoo",
        "message":root.getchildren()[1].text
      })
    #error
    else:
      lead_activity1.comment = "LMSstatus:2"
      lead_activity1.save()
      return JsonResponse({
        "LMSstatus":2,
        "additional":"Issue with Kookoo",
      })
  # Calling cofigration issue
  else:
    lead_activity1.comment = "LMSstatus:3"
    lead_activity1.save()
    return JsonResponse({
        "LMSstatus":3,
        "additional":"Calling is not activated please inform Admin",
        
      })

  



# kookoo
@csrf_exempt
def callDialKookoo(request):
  print("inddsadasdasd")
  datetime_of_request = datetime.datetime.now()
  
  telephonekookoo = TelePhonekookoo.objects.get(sid = request.GET['sid'])
  r1 = ""
  
  if request.GET.get('event','') == 'NewCall':
    r1=Response()
    print("calldial")
    if request.GET.get('mcid',''):
      lead = Lead.objects.get(id=request.GET.get('mcid',''))
      builder = BuilderCallInfo.objects.get(builder = lead.builder.id)
      r1.addDial(str_decode(telephonekookoo.phone.number),record='true',limittime="1000",timeout="30",moh='default',promptToCalledNumber='no',caller_id=builder.builder_call_info_kookoo.caller_id)
      telephonekookoo.status = "ConnectingVisitor"
      print("Call ********** ConnectingVisitor *********")
    else:
      print("issue with builder settings")


  elif request.GET.get('event','') == 'Dial' or request.GET.get('event','') == 'Hangup':
      if request.GET['status'] == 'not_answered':
        r1 = '<?xml version="1.0" encoding="UTF-8"?><root><status>Success</status><message>'+request.GET['status']+'</message></root>'
        if request.GET.get('message','') == "NormalCallClearing":
          telephonekookoo.status = "MissCallVisitor"
          print("Call ********** MissCallVisitor *********")
        elif request.GET.get('message','') == "NoAnswer":
          telephonekookoo.status = "RejectedVisitor"
          print("Call ********** RejectedVisitor *********")
         
        else:
          telephonekookoo.status = request.GET.get('message','') + "Visitor"
          print("Call **********" + request.GET.get('message','') + "Visitor *********")

          

      else:
        r1 = '<?xml version="1.0" encoding="UTF-8"?><root><status>Success</status><message>'+request.GET['status']+'</message></root>'

        if request.GET.get('message','') == "answered":
          telephonekookoo.status = "AnsweredVisitor"
          print("Call ********** AnsweredVisitor *********")
          telephonekookoo.url = request.GET.get('data','')
        else:
          telephonekookoo.status = request.GET['status'] + "Visitor"
          print("Call ********** " + request.GET['status'] + "Visitor *********")
      

    
  else:
    pass
  
    
  telephonekookoo.save()

  RequestLog.objects.create(
    requested_at = datetime_of_request,
    requested_method = 'GET',
    requested_response = r1,
    requested_errors = "",
    # requested_params = base64.b64encode(json.dumps(request.GET).encode()) ,
    requested_params = json.dumps(request.GET), # need to remve this in Production
    requested_url = 'Outgoing',
    user_remote_addr = request.META['REMOTE_ADDR'],
    user_host =  get_current_site(request).domain + request.path_info,
    response_sid = request.GET['sid'],
  )
  
  return HttpResponse(r1)





# incomming
@csrf_exempt
def inboundCallKookoo(request):
  print("________________________________________________INcoming_________________________________ ",request.GET)
  r1 = ""
  datetime_of_request = datetime.datetime.now()

  if request.GET.get('event') =='NewCall':
    builders = BuilderCallInfo.objects.filter(builder_call_info_kookoo__caller_id = request.GET.get('called_number'))

    # The following code support muiltiple Builder sharing same DID and selects first mached Lead
    phonecount = 0
    for eachbuilder in builders:
      query = Q()
      query_phone_model = PhoneNumber.objects.filter( builder=eachbuilder.builder).filter(number=str_encode(request.GET.get('cid_e164')[3:],True))
      builder = eachbuilder
      if query_phone_model.count() > 0:
        break

    if query_phone_model.count() > 0:
      phone_model = query_phone_model.first()
      lead = query_phone_model.first().lead_set.first()
      if lead:
        agent2 = lead.tme.phone
        cid = lead.id
      else:
        print("phone is not linked with lead")


      telePhonekookoo1 = TelePhonekookoo.objects.create(
        sid = request.GET.get('sid'),
        user =  lead.tme,
        lead = lead.id,
        phone = phone_model,
        status = "ConnectingAgent",
        call_type = "In"
      )

      # import pdb ; pdb.set_trace()
      lead_activity1 = LeadActivity(
                activity_type = 'telephone_incomming',
                remote_addr = request.META['REMOTE_ADDR'],
                remote_url_requested = '/telephone/kookoo/inboundcall/',
      )
      lead_activity1.user = lead.tme
      lead_activity1.telephone = telePhonekookoo1 
      lead_activity1.save()
      lead.lead_activity.add(lead_activity1)
      lead.last_lead_activity = lead_activity1
      lead.save()

      r1=Response()
      r1.addDial(agent2,record='true',limittime="1000",timeout="30",moh='default',promptToCalledNumber='no',caller_id=builder.builder_call_info_kookoo.caller_id)

    else:
      r1=Response()
      r1.addDial(CustomUser.objects.get(name="Kamala").phone,record='true',limittime="1000",timeout="30",moh='default',promptToCalledNumber='no',caller_id=request.GET.get('called_number'))

      print("New call")
      
  elif request.GET.get('event') =='Dial'or request.GET.get('event','') == 'Hangup':
      telephonekookoo = TelePhonekookoo.objects.get(sid = request.GET['sid'])
      if request.GET['status'] == 'not_answered':
        if request.GET.get('message','') == "NormalCallClearing":
          telephonekookoo.status = "MissCallAgent"
          print("Call ********** MissCallAgent *********")
        elif request.GET.get('message','') == "NoAnswer":
          telephonekookoo.status = "RejectedAgent"
          print("Call ********** RejectedAgent *********")
         
        else:
          telephonekookoo.status = request.GET.get('message','') + "Agent"
          print("Call **********" + request.GET.get('message','') + "Agent *********")

      else:

        if request.GET.get('message','') == "answered":
          telephonekookoo.status = "AnsweredAgent"
          print("Call ********** AnsweredAgent *********")
          telephonekookoo.url = request.GET.get('data','')
        else:
          telephonekookoo.status = request.GET['status'] + "Agent"
          print("Call ********** " + request.GET['status'] + "Agent *********")


      telephonekookoo.save()
  else:
    pass

  RequestLog.objects.create(
    requested_at = datetime_of_request,
    requested_method = 'GET',
    requested_response = r1,
    requested_errors = "",
    # requested_params = base64.b64encode(json.dumps(request.GET).encode()) ,
    requested_params = json.dumps(request.GET) ,
    requested_url = 'incomming',
    user_remote_addr = request.META['REMOTE_ADDR'],
    user_host =  get_current_site(request).domain + request.path_info,
    response_sid = request.GET.get('sid',''),
  )

  return HttpResponse(r1)

