
import datetime

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.views import View

from management.models import *
from dashboard.models import *
from inbound.models import *
from telephone.models import *

from inbound.service import *

# from notifcation.service import notifcationRefresh
import requests
from urllib.parse import unquote
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

import calendar
import datetime
from django.db.models import Q

from management.customencryption import *
from dashboard.tableresponse import *

#Decorater  Login_autentication  to check
def Login_autentication(checking_function):
    def loginauth(request,*args, **kwds):
        if not request.request.user.is_authenticated:
            return redirect('../login/')
        else:
            return checking_function(request, *args, **kwds)
    return loginauth



# login Page handling class
class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if (user is not None):
            if user.is_active:
                if user.is_superuser:
                    login(request, user)
                    request.session['userid'] = user.id
                    return redirect('/')


                elif (not user.builder):
                    return render(request, 'login.html', {
                    'error_message': 'Your account has been disabled because Builder is not Activated'
                    })


                elif user.builder.pk == 'FA0001':
                    login(request, user)
                    request.session['userid'] = user.id
                    return redirect('/')


                elif not user.builder.service:
                    return render(request, 'login.html', {
                    'error_message': 'Your account has been disabled because Servive is not Activated'
                    })

                else:
                    login(request, user)
                    request.session['userid'] = user.id
                    return redirect('/')

            else:
                return render(request, 'login.html', {
                    'error_message': 'Your account has been disabled'
                    })
        else:
            return render(request, 'login.html', {
                'error_message': 'Invalid login credentials'
                })


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('/login/')


class Home(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login/')
        else:
            if request.user.is_superuser:
                return redirect('../superadmin/')
            if request.user.user_roles.ui_type == 'ED':
                return redirect('../lead/new_lead/')
            elif request.user.user_roles.ui_type == 'MA':
                return redirect('../management/live_chats/')

class Settings(View):
    def get(self,request):
        user = CustomUser.objects.get(pk = request.session['userid'])
        context = {
                    "userid": user.pk,
                    "userName":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "phone":user.phone,
                    "mailid":user.email,
                    "address":user.address,
                    'USER': user.username + ' (' +user.user_roles.name + ')'
                  }
        return render(request, './settings.html',context)


    def post(self,request):
        user = CustomUser.objects.get(id = request.session['userid'])
        # user =

        if user.pk == int(request.POST['id']):
            if request.POST['username'] != 'None':
                user.username = request.POST['username']
            else:
                return JsonResponse({'Status':'Required Filed Username'})

            if request.POST['password'] != '':
                user.set_password(request.POST['password'])

            if request.POST['first_name'] != 'None':
                user.first_name = request.POST['first_name']

            if request.POST['last_name'] != 'None':
                user.last_name = request.POST['last_name']

            if request.POST['phone'] != 'None':
                user.phone = request.POST['phone']

            if request.POST['mailid'] != 'None':
                user.mailid = request.POST['mailid']

            if request.POST['address'] != 'None':
                user.address = request.POST['address']

            user.save()

        else:
            return JsonResponse({'Status':'Required Filed Username'})
        return JsonResponse({'Status':'Saveed Successfull'})




class Leads(View):
    @Login_autentication
    def get(self,request,slug):
        # slug
        user = CustomUser.objects.get(pk = request.session['userid'])
        if user.builder.id == 'FA0001':
            builders = Builder.objects.exclude(id = user.builder.id)
            property_list = Project.objects.exclude(builder = user.builder.id)
        else:
            builders = []
            property_list = Project.objects.filter(builder = user.builder.id)
        
        lead_status_list = LeadStatus.objects.filter(status_type  = "Negative")
        call_status_list =  CallStatus.objects.all()


        context = {
            'subtitle' : ' '.join([each.capitalize() for each in slug.split('_')]),
            'projects_list' : property_list,
            'builder_list':builders,
            'builder':user.builder,
            'call_status_list':call_status_list,
            'lead_status_list':lead_status_list,
            'agent_type' : user.user_roles.user_type,
            'agent_type_list' :  ['FT','FB','FTB'],
            'USER': user.username + ' (' +user.user_roles.name + ')',
            'page':slug
        }
        # notifcationRefresh(request.session['userid'])
        return render(request, 'lead.html',context)



    @Login_autentication
    def post(self,request):


        listofdata = []
        postRequest = dict(request.POST)

        query = Q()

        # date
        if postRequest['startdate'][0] and postRequest['enddate'][0]:
            datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
            dateend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
            query = Lead.objects.filter(source_date__gte = datestart).filter(source_date__lte = dateend)

        elif postRequest['startdate'][0]:
            datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
            query = Lead.objects.filter(source_date = datestart)

        elif postRequest['enddate'][0]:
            datestart = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
            query = Lead.objects.filter(source_date = datestart)

        else:
            query = Lead.objects.all()


        page =  request.POST['page']

        if page ==  "new_lead":
            query = query.filter(last_lead_activity__lead_status__status_type = "Initial")

        elif page == "follow_up":
            query = query.filter(last_lead_activity__lead_status__status_type = "Intermediate")

        elif page == "completed":
            query = query.filter(last_lead_activity__lead_status__status_type = "Finish")

        else:
            query = query.filter(last_lead_activity__lead_status__status_type = "Negative")

        # user
        user = CustomUser.objects.get(pk = request.session['userid'])
        query = query.filter( tme = user)
        query = query.filter( builder__is_active = True)


        # builder
        if postRequest.get('builders',''):
            query1 = Q()
            for eachbuilder in postRequest['builders']:
                query1 |= Q(builder = eachbuilder)
            query = query.filter(query1)

        # projects
        if postRequest.get('projects',''):
            query1 = Q()
            for eachprojects in postRequest['projects']:
                query1 |= Q(project = eachprojects)
            query = query.filter(query1)


        # call_status
        if postRequest.get('call_status',''):
            query1 = Q()
            for eachprojects in postRequest['call_status']:
                query1 |= Q(last_lead_activity__call_status__id = eachprojects)
            query = query.filter(query1)


        # lead_status
        if postRequest.get('lead_status',''):
            query1 = Q()
            for eachprojects in postRequest['lead_status']:
                query1 |= Q(last_lead_activity__lead_status__id = eachprojects)
            query = query.filter(query1)



        if request.POST['search']:
            query1 = Q()
            query1 |= Q(visitor_id__icontains = postRequest['search'][0])
            query1 |= Q(name__icontains = postRequest['search'][0])
            query = query.filter(query1)


        recordsTotal = query.count()

        start = int(postRequest['start'][0])
        stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

        dataofeachproject = ['visitor_id','source_date','name']

        if request.POST['orderDir'] == "desc":
            query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
        else:
            query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

        query = query[start:stop]

        for oj in query:
            dataofeachproject = []
            dataofeachproject.append(str(oj.visitor_id))
            dataofeachproject.append(oj.source_date)
            dataofeachproject.append(oj.name)
            dataofeachproject.append(oj.builder.name + '<br/>' + oj.project.name)

            lead_status = ""
            if oj.last_lead_activity.lead_status:
                lead_status += oj.last_lead_activity.lead_status.name + "<br/>" 
            else:
                lead_status += "<br/>"
            if oj.last_lead_activity.call_status:
                lead_status += oj.last_lead_activity.call_status.name + "<br/>" 
            else:
                lead_status += "<br/>"
            
            if oj.last_lead_activity.comment:
                lead_status += oj.last_lead_activity.comment


            dataofeachproject.append( lead_status)
            dataofeachproject.append(" <button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='edit("+str(oj.pk)+")'>Edit</button>")
            listofdata.append(dataofeachproject)
        context = {
        "aaData":listofdata,
        "recordsTotal":recordsTotal,
        "recordsFiltered":recordsTotal,
        }
        return JsonResponse(context)







class LeadEdit(View):
    @Login_autentication
    def get(self,request):
        lead = Lead.objects.get(pk=request.GET['id'])
        lead_status_list = lead.builder.service.status.all()
        visitor_phone = lead.phone.all()
        if len(visitor_phone) == 0:
            call_status_list = CallStatus.objects.filter(id=8)
        else:
            call_status_list = []

        call_status_list = CallStatus.objects.exclude(name="None") # need remove 

        chatmessages = ''
        if lead.live_chat.all()[0].chat_url is None or lead.live_chat.all()[0].chat_url:
            livechat = lead.live_chat.all()[0] 
            livechat.chat_url = (
                'http://{server_id}/livserv/viewchat/getChatMsgTasklist.jsp?chVisitid={visitor_id}&comp_code={folder}&yr_month={source_date}'.format(
                    server_id = lead.live_chat.all()[0].server_id.name ,
                    visitor_id = lead.visitor_id,
                    folder = '-'.join(lead.live_chat.all()[0].folder.name.split('-')[:2]),
                    source_date = '-'.join([lead.source_date.strftime('%Y'),lead.source_date.strftime('%m').lstrip("0")]),

                )

            )
            livechat.save()
            # pass
        #      =  (
        #                     'http://{server_id}/livserv/viewchat/getChatMsgTasklist.jsp?chVisitid={visitor_id}&comp_code={folder}&yr_month={source_date}'.format(
        #                         server_id = lead.live_chat.all()[0].server_id.name ,
        #                         visitor_id = lead.visitor_id,
        #                         folder = '-'.join(lead.live_chat.all()[0].folder.name.split('-')[:2]),
        #                         source_date = '-'.join([lead.source_date.strftime('%Y'),lead.source_date.strftime('%m').lstrip("0")]),                              
        #                     )
        #     lead.live_chat.all()[0].save()


        # import pdb; pdb.set_trace()


        r = requests.get(lead.live_chat.all()[0].chat_url)
        # print(lead.live_chat.all()[0].chat_url)
        if r.text.replace('\n','') != '<root></root>':
            tree = ET.fromstring(r.text.replace('\n','')) 
            metahtm = tree.getchildren()[0].getchildren()[0].getchildren()[1].text
            htmldata = unquote(metahtm)
            soup = BeautifulSoup(htmldata)
            metadata = {}
            for each in soup.find_all('tr')[1:]:
                metadata[each.find_all('td')[0].text.replace(' ','')] = each.find_all('td')[2].text

            metadata['chatmessage'] = []
            for each in tree.getchildren()[1:]:
                chatmessage = {}
                for each2 in each.getchildren():
                    chatmessage['time'] = each2.attrib['MTS']
                    chatmessage['person'] = each2.getchildren()[0].text
                    chatmessage['message'] = unquote(each2.getchildren()[1].text).replace('http%3A//','http://').replace(
                        "<font color='green'><b>The Current Page URL is : ",''
                    ).replace(
                        '</b></font>',''
                    )
                metadata['chatmessage'].append(chatmessage)
            chatmessages = metadata


        context = {
            'lead': lead,
            'visitor_phone':visitor_phone,
            'call_status_list2':call_status_list,
            'lead_activity_list':lead.lead_activity.all(),
            'lead_activity_list' : lead.lead_activity.all(),
            'lead_status_list':lead_status_list,
            'chatmessages':chatmessages,
            'unit_type_list':LeadType.objects.all(),
            'buying_reason_list':BuyingReason.objects.all(),
            'lead_source_list':Leadsource.objects.all()

        }
        return render(request, 'form.html',context)


    @Login_autentication
    def post(self,request):
        request_status = ""
        fielsChangedlist = []
        
        lead = Lead.objects.get(id=request.POST['id'])

        parameter1 = [
            'name', 'age', 'address', 'additional_info', 
            'from_unit_size', 'to_unit_size', 
            'from_budget', 'to_budget'
            ,'visit_date', 'designation'
        ]
        
        for eachparameter in parameter1:
            if request.POST[eachparameter] != 'None':
                if getattr(lead,eachparameter) != request.POST[eachparameter]: 
                    fielsChanged = FielsChanged.objects.create(
                        feilds = eachparameter,
                        old_data = getattr(lead,eachparameter),
                        new_data = request.POST[eachparameter]
                    )
                    fielsChangedlist.append(fielsChanged)
                    setattr(lead,eachparameter,request.POST[eachparameter])


        parameter2 = {
            'country':'Country',
            'city':'City',
           
        }

        from management import models as model_s
        for eachparameter in parameter2.keys():
            if request.POST[eachparameter] != 'None':
                model = getattr(model_s, parameter2[eachparameter])
                model_each, created_flag  = model.objects.get_or_create(
                    name = request.POST[eachparameter]
                )
                if created_flag:
                    fielsChanged = FielsChanged.objects.create(
                        feilds = eachparameter,
                        old_data = getattr(lead,eachparameter),
                        new_data = request.POST[eachparameter]
                    )
                    fielsChangedlist.append(fielsChanged)
                    setattr(lead,eachparameter,model_each)
        
        
        parameter3 = {
            'unit_type':'UnitType',
            'lead_source':'Leadsource',
            'buying_reason':'BuyingReason'
        }

        for eachparameter in parameter3.keys():
            if request.POST[eachparameter] != 'None' and request.POST[eachparameter].replace(" ","") != "": 
                model = getattr(model_s, parameter3[eachparameter])
                # import pdb; pdb.set_trace()
                print("asdsadasdasd",request.POST[eachparameter])
                model_each = model.objects.get(id = int(request.POST[eachparameter]))
                if  getattr(lead,eachparameter) != model_each:
                    fielsChanged = FielsChanged.objects.create(
                        feilds = eachparameter,
                        old_data = getattr(lead,eachparameter).name,
                        new_data = request.POST[eachparameter]
                    )
                    fielsChangedlist.append(fielsChanged)
                    setattr(lead,eachparameter,model_each)
                    
 
        # phone
        phoneno = request.POST['phoneno']
        if phoneno != 'None':
            phone_info = Create_Muiltiple("PhoneNumber",phoneno,lead.builder)
            if len(phone_info) > 0:
                lead.phone.add(*phone_info)
                fielsChanged = FielsChanged.objects.create(
                    feilds = 'phone',
                    new_data =  str_encode(phoneno,True) 
                )
                fielsChangedlist.append(fielsChanged)
                    

        # mail
        mailid = request.POST['mailid']
        if mailid != 'None':
            mail_info = Create_Muiltiple("Emailaddress",mailid,lead.builder)
            if len(mail_info) > 0:
                lead.email.add(*mail_info)
                fielsChanged = FielsChanged.objects.create(
                        feilds = 'email',
                        new_data = str_encode(mailid,True) 
                    )
                fielsChangedlist.append(fielsChanged)


        if request.POST['sid'] != 'None' and request.POST['sid'] !='':
            lead_activity1 = LeadActivity.objects.filter(telephone__sid=request.POST['sid']).last()
            if request.POST['leadComment'] != 'None':
                if lead_activity1.comment:
                    lead_activity1.comment = lead_activity1.comment  +  request.POST['leadComment'] 
                else:
                    lead_activity1.comment = request.POST['leadComment'] 
            
        
        else:
            lead_activity1 = LeadActivity.objects.create(
                activity_type = 'other',
                remote_addr = request.META['REMOTE_ADDR'],
                remote_url_requested = request.META['HTTP_REFERER'],
                user =  CustomUser.objects.get(pk = request.session['userid'])
                
            )   
            if request.POST['leadComment'] != 'None':
                lead_activity1.comment = request.POST['leadComment'] 

        lead_activity1.call_status = CallStatus.objects.get(id = request.POST['CallStatusSelect'])
        lead_activity1.lead_status =  LeadStatus.objects.get(id =request.POST['leadStatusSelect'])

        if request.POST['enquiryDate'] != 'None':
            lead_activity1.next_enquiry_date = request.POST['enquiryDate']

        

        lead_activity1.save()
        
        if len(fielsChangedlist) != 0:
            lead_activity1.fiels_changed.add(*fielsChangedlist)

        lead_activity1.save()
        
        lead.lead_activity.add(lead_activity1)

        lead.last_lead_activity = lead_activity1

        lead.save()
        context = {
                "Status": request_status,
            }
        return JsonResponse(context)





class LeadDataLoad(View):
    @Login_autentication
    def get(self,request,slug):
        if slug == "LeadStatus":
            callStatusSelected = request.GET.get('callStatusSelected','')
            lead = request.GET.get('leadid')
            servicetype = Lead.objects.get(id=lead).builder.service
            print(servicetype)
            context = {
                "leadstatuslist": [
                    {
                        "id":0,
                        "option":"Select"
                    },

                ]
            }
            if callStatusSelected != '':
                callstatusLeadstatus = CallstatusLeadstatus.objects.filter(call_status=callStatusSelected,service=servicetype).first()
                for each in callstatusLeadstatus.lead_type.all():
                    context["leadstatuslist"].append(
                        {
                            "id":each.pk,
                            "option":each.name
                        }
                    )

            return JsonResponse(context)

        elif slug == "leadStatusEnquiryDate":

            if LeadStatus.objects.get(id=request.GET.get('leadStatusSelect')).status_type == "Intermediate":
                status = True
            else:
                status = False
            context = {
                "Status": status,

                
            }
            return JsonResponse(context)



class Managements(View):

    header_reports_list = ['ID', 'Lead No', 'Name', 'Chat Date', 'Builder', 'Project', 'Chat', 'Lead Status List', 'Call Status List','Related Data List',  ]

    @Login_autentication
    def get(self,request,slug):
        context = {}
        user=CustomUser.objects.get(pk=request.session['userid'])
        if user.user_roles.ui_type != "MA":
            return redirect('../lead/new_lead/')

        builders_list = Builder.objects.exclude(id = 'FA0001')
        property_list = Project.objects.exclude(builder__id = 'FA0001')
        lead_status_list = LeadStatus.objects.all()
        call_status_list =  CallStatus.objects.all()
        typelistagent = ['FT','FB','FTB']
        agent_list = CustomUser.objects.filter(user_roles__user_type__in=typelistagent)

        context['subtitle'] = ' '.join([each.capitalize() for each in slug.split('_')])
        context['projects_list'] = property_list
        context['builder_list'] = builders_list
        context['call_status_list'] = call_status_list
        context['lead_status_list'] = lead_status_list
        context['projects_list'] = property_list
        context['user'] = user
        context['agent_type_list'] = ['FT','FB','FTB','FA']
        context['page'] = slug
        context['agent_list'] = agent_list
        context['filter_show'] = True

        # slug
        if(slug == "graphs"):
            return render(request, 'Management/graphs/lead.html',context)
                
        elif(slug == "reports"):
            context['header_list'] = [
                # 'ID', 
                'Lead No',
                'Chat Date', 
                'Name', 
                'Builder : Project', 
                'TME',   
                'Call Status : Lead Status',
                'Reason',
                'Related Data',
                'Modified'
                # 'Call Status List',
                # 'Related Data', 
                # ,'Chat'
                ]
 
            context['sortable_list'] = '6,7'  
            return render(request, 'Management/reports/lead.html',context)
            
        elif(slug == "agents_activity"):
            context['header_list'] = [
                'ID', 'Chat Date', 'Lead No', 'Name', 
                'Builder : Project', 
                'Lead Status List','Call Status List','Agent',"Modified", 'Related Data List'
                # ,'Chat'
                ]

            context['sortable_list'] = '2,6,7,8,9'  
            return render(request, 'Management/agents_activity/lead.html',context)
        
        elif(slug == "lead_assign"):
            context['header_list'] = [
                'ID', 'Lead No', 'Chat Date',  'Name', 
                'Builder : Project', 
                'Lead Status List','Call Status List' ,'TME Agent','Select TME','Action'
                # ,'Chat'
                ]

            context['sortable_list'] = '2,6,7,8,9'  
            context['page'] = "lead_assign"
            return render(request, 'Management/lead_assign/lead.html',context)
        
      
        elif(slug == "live_chats" ):
            context['header_list'] = [
                'Lead No','Requested At',
                'Response Time(ms)','Path',
                'Remote Address','Host','Response',
                'Status Code','Errors']
            context['sortable_list'] = '2,6,7,8,9'  
            context['project_show'] = False
            context['builder_show'] = False

            return render(request, 'Management/tracking/tracking.html',context)

        elif(slug == "cron" ):
            context['header_list'] = [
                'Id','Start At','Ends At',
                'Message','Run Time','Success',
                ]
            context['sortable_list'] = '1'  
            context['project_show'] = False
            context['builder_show'] = False
            return render(request, 'Management/tracking/tracking.html',context)
        
        elif(slug == "emails"):
            context['header_list'] = ['id','usermail_id','builder','status_error','created','Action']
            context['sortable_list'] = '1'  
            context['builder_show'] = True
            context['project_show'] = False
            return render(request, 'Management/tracking/tracking.html',context)    

        elif(slug == "phone"):
            context['header_list'] = ['Phone id','number','builder','status_error','created','Action']
            context['sortable_list'] = '1'  
            return render(request, 'Management/tracking/tracking.html',context)   
    
        # elif(slug == "onboarding_builders"):
        #     pass

        elif(slug == "profile"):
            user = CustomUser.objects.get(pk = request.session['userid'])
            context = {
                        "userid": user.pk,
                        "userName":user.username,
                        "first_name":user.first_name,
                        "last_name":user.last_name,
                        "phone":user.phone,
                        "mailid":user.email,
                        "address":user.address,
                        'USER': user.username + ' (' +user.user_roles.name + ')'
                    }
            return render(request, 'Management/profile/settings.html',context)
        
        elif(slug == "users"):
            context['filter_show'] = False
            context['header_list'] = ['id','User Name','First Name','Last Name','Phone','Email','Action']
            context['sortable_list'] = '1'  
            return render(request, 'Management/tracking/tracking.html',context) 

        elif(slug == "users_edit"):
            return render(request, 'Management/tracking/form.html',{"dsa":"as"}) 

        elif(slug == "builders"):
            context['filter_show'] = False
            context['header_list'] = [
                'id','Name','package','limit_reached',
                'start_date','is_livprop_tranfer','is_encryption',
                'is_auto_assign_tme', 'service', 'is_active', 'created'
                ]
            context['sortable_list'] = '1'  
            return render(request, 'Management/tracking/tracking.html',context) 


        elif(slug == "builders_api"):
            context['filter_show'] = False
            context['header_list'] = [
                'id','Name','package','limit_reached',
                'start_date','is_livprop_tranfer','is_encryption',
                'is_auto_assign_tme', 'service', 'is_active', 'created'
                ]
            context['sortable_list'] = '1'  
            return render(request, 'Management/tracking/tracking.html',context)

        elif(slug == "builders_mails"):
            context['header_list'] = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']
            context['sortable_list'] = '2,6,7,8,9'  
            return render(request, 'Management/tracking/tracking.html',context)
        elif(slug == "builders_API"):
            context['header_list'] = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']
            context['sortable_list'] = '2,6,7,8,9'  
            return render(request, 'Management/tracking/tracking.html',context)

     

       
        # elif(slug == "leads" ):
        #     context['header_list'] = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']
        #     context['sortable_list'] = '2,6,7,8,9'  
        #     return render(request, 'Management/tracking/tracking.html',context)
      
      
      
        elif(slug == "project_priority" ):
            context['header_list'] = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']
            context['sortable_list'] = '2,6,7,8,9'  
            return render(request, 'Management/tracking/tracking.html',context)

        # general edits 

        elif(slug == "agent" ):
            context['header_list'] = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']
            context['sortable_list'] = '2,6,7,8,9'  
            return render(request, 'Management/tracking/tracking.html',context)

            

    @Login_autentication
    def post(self,request,slug):
        if(slug == "chartajax" ):
            return JsonResponse(chartajaxView(request))

        elif(slug == "reports" ):
            return JsonResponse(reportView(request))

        elif(slug == "agents_activity"):
            return JsonResponse(agents_activityView(request)) 

        elif(slug == "live_chats" ):
            return JsonResponse(live_chatsView(request))

        elif(slug == "cron"):
            return JsonResponse(cronView(request))
      
        elif(slug == "emails"):
            return JsonResponse(emailsViews(request))
        
        elif(slug == "phone"):
            return JsonResponse(phoneViews(request))
        
        elif(slug == "users"):
            return JsonResponse(UserViews(request))
        
        elif(slug == "builders"):
            return JsonResponse(buildersViews(request))
        
        elif(slug == "builders_api"):
            return JsonResponse(buildersApiViews(request))
        
        elif(slug == "lead_assign"):
            return JsonResponse(Lead_assignViews(request))

        elif(slug == "lead_assign_save"):
            return JsonResponse(Lead_assign_saveViews(request))
        
            