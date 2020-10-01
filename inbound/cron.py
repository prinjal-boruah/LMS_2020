from django_cron import CronJobBase, Schedule
from management.models import *
from inbound.models import *
from management.customencryption import *
import datetime 
from django.utils import timezone
import pytz
import logging
from management.start import createNewInstance
logger = logging.getLogger(__name__)
import re
import phonenumbers
from inbound.service import *
import json
# from outbound.models import PushFlags


# every 1 min
class LeadTranfer(CronJobBase):
    RUN_EVERY_MINS = 1
    ALLOW_PARALLEL_RUNS = False
    MIN_NUM_FAILURES = 3
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'inbound.LeadTranfer'

    def do(self):

        leads = APILead.objects.filter(flag=False)
        print(len(leads))

        oldlead = Lead.objects.all()

        
        lead_alerady = [eachlead.visitor_id for eachlead in oldlead]
        count = 0

        for eachlead in leads:
            if eachlead.chVisitid not in lead_alerady:
                lead_alerady.append(eachlead.chVisitid)
                print('Tranfer : ',"******************************************:",count)
                print('Tranfer : ',eachlead.chVisitid)
                count += 1
                # create or get 
                # builder
                builder_model, builder_created_flag = Builder.objects.get_or_create( id = eachlead.compid )
                # ~create
                if builder_created_flag:
                    builder_model.name = eachlead.cmpname
                    builder_model.start_date = datetime.datetime.now().date()
                    builder_model.package = Package.objects.get(name='default')
                    builder_model.is_active = True
                    builder_model.service = Service.objects.get(name = 'Site Visit')
                    builder_model.save()

                print('Tranfer : ',"builder")
                # builder_model.is_active = True
                # builder_model.save() #need to remvoe

                # New builder configration with out activation you can't proceed
                if builder_model.is_active == False:
                    errordata = dict()
                    errordata['Builder__is_active'] = False
                    eachlead.status_error = json.dumps(errordata)
                    eachlead.save()

                else:
                    print('Tranfer : ',"builder old")

                    lead = Lead()

                    lead.visitor_id =  eachlead.chVisitid
                    # import pdb; pdb.set_trace()
                    lead.source_date = datetime.datetime.strptime(eachlead.leadDate[0:10],'%Y-%m-%d').date()
                    lead.builder = builder_model
                    
                    print('Tranfer : ',"Lead")

                    # project
                    project_model, project_created_flag  = Project.objects.get_or_create(
                        id =  eachlead.propid
                    )
                    # ~create
                    if project_created_flag:
                        project_model.name =  eachlead.property
                        project_model.builder = builder_model
                        project_model.save()

                    lead.project = project_model   

                    print('Tranfer : ',"Project")

                    # country
                    if eachlead.country:
                        # ~create or get
                        country_model, country_created_flag  = Country.objects.get_or_create(
                            name =  eachlead.country
                        )
                        lead.country = country_model

                    print('Tranfer : ',"Country")


                    # city
                    if eachlead.city:
                        # ~create or get
                        city_model, city_created_flag  = City.objects.get_or_create(
                            name =  eachlead.city
                        )
                        lead.city = city_model
                        
                    print('Tranfer : ',"City")
                    
                    # LiveChat Create

                    live_chat_model = LiveChat()
                    print('Tranfer : ',"LiveChat")

                    #  web_site_url
                    if eachlead.websiteurl:
                        print('Tranfer : ',eachlead.websiteurl)
                        # ~create or get
                        websiteurl_model, web_site_url_created_flag  = WebSiteUrl.objects.get_or_create(
                            name =  eachlead.websiteurl
                        )
                        live_chat_model.web_site_url = websiteurl_model
                    
                    print('Tranfer : ',"WebSiteUrl")
                    
                    # source
                    if eachlead.source:
                        print('Tranfer : ',eachlead.source)
                        # ~create or get
                        source_model, source_created_flag  = Source.objects.get_or_create(
                            name =  eachlead.source
                        )
                        live_chat_model.source = source_model
                    
                    print('Tranfer : ',"Source")

                    # folder
                    if eachlead.fldrname:
                        print('Tranfer : ',eachlead.fldrname)
                        # ~create or get
                        fldrname_model, folder_created_flag  = Folder.objects.get_or_create(
                            name =  eachlead.fldrname
                        )
                        live_chat_model.folder = fldrname_model

                    print('Tranfer : ',"Folder")

                    # server_id
                    if eachlead.serverid:
                        # ~create or get
                        serverid_model, server_id_created_flag  = ServerId.objects.get_or_create(
                            name =  eachlead.serverid
                        )
                        live_chat_model.server_id = serverid_model

                    print('Tranfer : ',"ServerId")

                    # additional
                    if eachlead.additional:
                        live_chat_model.additional = eachlead.additional

                    print('Tranfer : ',"additional")
                    
                    live_chat_model.save()

                    lead.save()

                    lead.live_chat.add(live_chat_model)

                    if eachlead.customerName:
                        lead.name =  eachlead.customerName
                    
                    print('Tranfer : ',"customerName")

                    print('Tranfer : ','lead created')

                    # chat_url genration 
                    try:
                        # needto change the source_date
                        live_chat_model.chat_url = (
                            'http://{server_id}/livserv/viewchat/getChatMsgTasklist.jsp?chVisitid={visitor_id}&comp_code={folder}&yr_month={source_date}'.format(
                                server_id = serverid_model.name,
                                visitor_id = lead.visitor_id,
                                folder = '-'.join(fldrname_model.name.split('-')[:2]),
                                source_date = '-'.join([lead.source_date.strftime('%Y'),lead.source_date.strftime('%m').lstrip("0")])))
                        
                        live_chat_model.save()
                        print('Tranfer : ','chat_url created')

                    except:
                        if eachlead.status_error:
                            errordata = json.loads(eachlead.status_error)
                        else:
                            errordata = dict()
                        errordata['chat_url'] = True
                        eachlead.status_error = json.dumps(errordata)
                        eachlead.save()

                    
                    phone_info = Create_Muiltiple('PhoneNumber',eachlead.visphone,builder_model)
                    print('Tranfer : ',"PhoneNumber")
                    mail_info =  Create_Muiltiple('Emailaddress',eachlead.visemail,builder_model)
                    print('Tranfer : ',"Emailaddress")


                    print('Tranfer : ',phone_info)
                    if len(phone_info) > 0:
                        lead.phone.add(*phone_info)

                    print('Tranfer : ',mail_info)
                    if len(mail_info) > 0:
                        lead.email.add(*mail_info)


                    lead_activity = LeadActivity.objects.create(
                        lead_status =  LeadStatus.objects.get(status_type='Initial'),
                        activity_type = 'system',
                        remote_addr = '127.0.0.1',
                        remote_url_requested = '127.0.0.1',
                        comment = "From Chat server"
                        )
                    

                    lead.lead_activity.add(lead_activity)

                    lead.last_lead_activity = lead_activity

                    lead.save()

                    # PushFlags.objects.create(
                    #     lead = lead
                    # )

                    # lead_activity.created = DashboardLead.objects.filter(leadno = eachlead.chVisitid).last().created
                    
                    # lead_activity.save()



                    print('Tranfer : ','lead_activity created')

                    eachlead.flag = True
                    print('Tranfer : ','flag True')

                    eachlead.save()

            else:
                print("===========================repeted==================")

                    








class AutoAssign(CronJobBase):
    RUN_EVERY_MINS = 1
    ALLOW_PARALLEL_RUNS = False
    MIN_NUM_FAILURES = 3
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'inbound.AutoAssign'

    def do(self):
        leads = Lead.objects.filter(tme__isnull=True).filter(builder__is_auto_assign_tme=True)
        # print(leads)
        for eachlead in leads:
            builder_model = eachlead.builder
            lastday = datetime.timedelta(days=int(builder_model.package.validity_days))
            if ((builder_model.start_date + lastday) > datetime.datetime.now().date()):
                # lead Limitation
                if builder_model.limit_reached < builder_model.package.lead_limit:
                    builderAutoAssignInfo, builderAutoAssign_created_flag  = BuilderAutoAssignInfo.objects.get_or_create(
                                                                                        builder=builder_model,
                                                                            )

                    if builder_model.is_livprop_tranfer:
                        agents_list = CustomUser.objects.filter(
                                user_roles__user_type = 'FT'
                            ).filter(
                                is_active = True
                            ).order_by('pk')
                        
                    
                    else:
                        agents_list = CustomUser.objects.filter(
                                user_roles__user_type = 'CT'
                            ).filter(
                                is_active = True
                            ).order_by('pk')
                        eachlead.is_livprop_tranfer = False
                        eachlead.save()
                    

                    # if builderAutoAssign_created_flag:
                    #     builderAutoAssignInfo.last_tme = agents_list[2]
                    #     builderAutoAssignInfo.save()



                    if len(agents_list) > 0:
                        # lastone
                        if builderAutoAssignInfo.last_tme:
                            # print('last_tme found')
                            last_agent = builderAutoAssignInfo.last_tme # old is already assigied 
                            if last_agent not in agents_list :
                                last_agent = agents_list[len(agents_list)-1] 
                        else:
                            # print('last_tme not found')
                            last_agent = agents_list[len(agents_list)-1] #if last assigned is null 
                        
                        
                        # agents_list_pk
                        agents_list_pk =  list(map(lambda agents_list: agents_list.pk,agents_list))

                 
                        # avilabitly or list of absent 
                        agentAvilable = AgentAvailability.objects.filter(
                                agent__pk__in = agents_list_pk
                            ).filter(
                                from_date__lte =  timezone.now()
                            ).filter(
                                to_date__gte =  timezone.now()
                            )
                        
                        agentAvilable_list_pk =  list(map(lambda agentAvilable_list: agentAvilable_list.agent.id,agentAvilable))
                        print(agentAvilable_list_pk)
                        # priority
                        agentpriority = LeadAssignPriority.objects.filter(
                                agent__pk__in = agents_list_pk
                            ).filter(
                                from_date__lte =  timezone.now()
                            ).filter(
                                to_date__gte =  timezone.now()
                            ).filter(
                                projects__in = [eachlead.project]
                            )

                        agentpriority_list_pk =  list(map(lambda agentpriority_list: agentpriority_list.agent.id,agentpriority))

                   
                        # relisting
                        agents_list_pk = agents_list_pk[agents_list_pk.index(last_agent.id) :] + agents_list_pk[:agents_list_pk.index(last_agent.id) ] 
                        agents_list_pk = agents_list_pk[1:] + agents_list_pk[:1]

                        # removing_apsent 
                        agents_list_pk = [user for user in agents_list_pk if user not in agentAvilable_list_pk]


                        agenttoassign_pk = agents_list_pk[0]
                        
                        updatelast = False
                        if len(agentpriority_list_pk) > 0:
                            for eachuser in agents_list_pk:
                                for each_agentpriority in agentpriority_list_pk:
                                    if each_agentpriority == eachuser:
                                        agenttoassign_pk = each_agentpriority
                                        updatelast = True
                                        break
                     
                        else:
                            for eachuser in agents_list_pk:
                                agentcheck = LeadAssignPriority.objects.filter(
                                                agent__pk = eachuser
                                            ).exclude(
                                                projects__in = [eachlead.project]
                                            )
                                if len(agentcheck) == 0:
                                    agenttoassign_pk = eachuser
                                    break
                                        


                        agenttoassign = CustomUser.objects.get( id=agenttoassign_pk )

                        print("project:",eachlead.project)
                        print("Agent",agenttoassign.username)

                        
                        lead_activity = LeadActivity.objects.create(
                                lead_status =  LeadStatus.objects.get(status_type='Initial'),
                                activity_type = 'system',
                                remote_addr = '127.0.0.1',
                                remote_url_requested = '127.0.0.1',
                                comment = agenttoassign.username + "(TME Agent) is assign automatically"
                            )
                            
                        eachlead.lead_activity.add(lead_activity)
                        eachlead.tme = agenttoassign
                        eachlead.last_lead_activity = lead_activity   
                        eachlead.save()


                        if updatelast:
                            builderAutoAssignInfo.last_tme = CustomUser.objects.get( id = agents_list_pk[0])
                        else:
                            builderAutoAssignInfo.last_tme = agenttoassign

                        builderAutoAssignInfo.save()

           
                        
                    else:
                        if eachlead.status_error:
                            errordata = json.loads(eachlead.status_error)
                        else:
                            errordata = dict()
                        errordata['NoAgents'] = True
                        eachlead.status_error = json.dumps(errordata)
                
                else:
                    if eachlead.status_error:
                        errordata = json.loads(eachlead.status_error)
                    else:
                        errordata = dict()
                    errordata['leadlimit'] = True
                    eachlead.status_error = json.dumps(errordata)
            else:
                if eachlead.status_error:
                        errordata = json.loads(eachlead.status_error)
                else:
                    errordata = dict()
                errordata['expired'] = True
                eachlead.status_error = json.dumps(errordata)
            eachlead.save()
