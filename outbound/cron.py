from django_cron import CronJobBase, Schedule
from datetime import timedelta 
import datetime
from django_common.helper import send_mail
from .models import * 
from management.models import *
from dashboard.models import *
import requests
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

class PushAPICron(CronJobBase):
	RUN_EVERY_MINS = 5
	ALLOW_PARALLEL_RUNS = False
	MIN_NUM_FAILURES = 3
	RUN_AT_TIMES = ['17:00']
	schedule = Schedule(run_at_times=RUN_AT_TIMES)
	# schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'outbound.PushAPICron'

	def do(self):
        leads =  PushFlags.objects.filter(api_flag = False)

        for eachleads in leads:
            pushAPI = PushAPI.objects.filter(project = eachleads.lead.project).filter(is_active = True)
            if len(pushAPI) == 0:
                break
            else:
                pushAPI = pushAPI[0]

            # condition of sending like all the leads or only completed leads
            if pushAPI.condition != "NO":
                if eachleads.lead.lead_activity.last().lead_status.name != 'Intersted For Site Visit':
                    break

            apistring = pushAPI.api_parametejsonstring

            list_of_info_to_push = [ 
                "*#*#*#*#first_name*#*#*#*#" , "*#*#*#*#last_name*#*#*#*#", 
                "*#*#*#*#phone*#*#*#*#","*#*#*#*#email*#*#*#*#",
                "*#*#*#*#projectName*#*#*#*#","*#*#*#*#Interested*#*#*#*#",
                "*#*#*#*#websiteurl*#*#*#*#"
                ]
					
            status = "Intersted For Site Visit" + eachleads.lead.lead_activity.last().comment
 
            replacing_info = [
                eachleads.lead.name,'',
                str_decode(eachleads.lead.phone),str_decode(eachleads.lead.email)
                eachleads.lead.project.name, "yes",
                eachleads.lead.lead_source.name
                
                ]
            
            for indexoflist,eachregular in enumerate(list_of_info_to_push):
                apistring = apistring.replace(eachregular,replacing_info[indexoflist])

            print(apistring)

            import requests
            payload = apistring
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
            }

            datetime_of_request = datetime.datetime.now()
            response = requests.request("POST", pushAPI.api_URL, data=payload, headers=headers)


            PushLog.objects.create(
                request_type = "RestAPI",
                requested_at = datetime_of_request,
                response_ms = response.elapsed.total_seconds(),
                requested_params = payload,
                requested_status_code = response.status_code,
                requested_method = response.request.method,
                requested_response = response.text,
                requested_errors = "",
                requested_url = pushAPI.api_URL
            )

            if response.status_code == 200:
                eachleads.api_flag = True
                eachleads.save()






class PushMailCron(CronJobBase):
    RUN_EVERY_MINS = 5
	ALLOW_PARALLEL_RUNS = False
	MIN_NUM_FAILURES = 3
	RUN_AT_TIMES = ['17:00']
	schedule = Schedule(run_at_times=RUN_AT_TIMES)
	# schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'outbound.PushAPICron'

	def do(self):
        leads =  PushFlags.objects.filter(mail_flag = False)

        for eachleads in leads:
            pushMail = PushMail.objects.filter(project = eachleads.lead.project).filter(is_active = True)
            
            if len(pushMail) == 0:
                break
            else:
                pushMail = pushMail[0]

            # condition of sending like all the leads or only completed leads
            if pushMail.condition != "NO":
                if eachleads.lead.lead_activity.last().lead_status.name != 'Intersted For Site Visit':
                    break

            sub = "Lead Information from Livprop"
			first_name=eachleads.lead.name
			last_name=""
			phone=str_decode(eachleads.lead.phone)
     		email=str_decode(eachleads.lead.email)
            projectName=eachleads.lead.project.name
            source=eachleads.lead.lead_source.name
            comments= = "Intersted For Site Visit" + eachleads.lead.lead_activity.last().comment
            
            body = """
            <!DOCTYPE html><html><head></head><body>
            <p>Dear&nbsp; Bhaskar Kanchan,</p>
            <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; following are the lead information.</p>
            <p>first_name: {}</p>
            <p>last_name: {}</p>
            <p>phone: {}</p>
            <p>email: {}</p>
            <p>projectName: {}</p>
            <p>source: {}</p>
            <p>comments: {}</p>
            <p>--&nbsp;</p>
            <p>Thanks and Regards</p>
            <p>Fulfilment Team, LivServ Technologies Pvt Ltd, 218, 2nd Floor, J P Royale, Sampige Road, Malleswaram, Bangalore - 560 003. www.livserv.com</p></body></html>
            """.format(first_name,last_name,phone,email,projectName,source,comments)

            backend = EmailBackend(
                host='mail.livprop.com',
                port=465,username='fulfillment@livprop.com',
                password='LMS@1234',
                use_tls=True,fail_silently=False
                )
            msg = EmailMultiAlternatives(
                sub,"", backend.username,
                pushMail.to_mail.split(","),
                ["fulfillment@livprop.com"],
                headers={'Message-ID':1},
                connection=backend
                )
            msg.attach_alternative(body, "text/html")
            msg.send()
     
            PushLog.objects.create(
                request_type = "Mail",
                requested_at = datetime.datetime.now(),
                response_ms = '',
                requested_params = ",".join(["mail:",first_name,last_name,phone,email,projectName,source,comments]),
                requested_status_code = "",
                requested_method = "",
                requested_response ="",
                requested_errors = "",
                requested_url = pushMail.to_mail
            )

            eachleads.mail_flag = True
            eachleads.save()
   
