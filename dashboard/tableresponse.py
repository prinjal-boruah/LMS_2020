from management.models import *
from dashboard.models import *

import calendar
import datetime
from django.db.models import Q
from management.mixin import APIRequestLog
from django_cron.models import CronJobLog
import base64
from management.customencryption import *

import datetime

def chartajaxView(request):
    XAxisList = []
    TotalLeadList = []
    NewLeadList = []
    CompletedLeadList = []
    FolloUpLeadList = []
    NonProspectLeadlist = []

    # now = datetime.datetime.now()
    localuser=CustomUser.objects.get(pk=request.session['userid'])

    query = Q()
    query = Lead.objects.all()

    postRequest = dict(request.POST)

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


    if postRequest.get('agent_list',False):
        query = query.filter(tme__in = postRequest['agent_list'])
    
    if postRequest.get('projects',False):
        query = query.filter(project__in = postRequest['projects'])

    if localuser.builder.id == '00000':
        query = query.filter(is_livprop_tranfer = True)

    if  postRequest['startdate'][0] and postRequest['enddate'][0]:
        dstart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        dend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()

    else:
        dstart = datetime.datetime.now().date() - datetime.timedelta(365*2)
        dend = datetime.datetime.now().date()

    
    # day
    if(dend-dstart).days < 60:
        # day month
        for each in range(0,(dend-dstart).days):

            courser_day = dstart + datetime.timedelta(each)

            TotalLeadList.append(query.filter(
                    source_date__day =  courser_day.day).filter(
                    source_date__month =   courser_day.month
                ).count())

            NewLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Initial").filter(
                    source_date__day =  courser_day.day).filter(
                    source_date__month =   courser_day.month
                ).count())

            CompletedLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Finish").filter(
                    source_date__day =  courser_day.day).filter(
                    source_date__month =   courser_day.month
                ).count())
        
        
            FolloUpLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Intermediate").filter(
                    source_date__day =  courser_day.day).filter(
                    source_date__month =   courser_day.month
                ).count())
            
            NonProspectLeadlist.append(
                query.filter(last_lead_activity__lead_status__status_type = "Negative").filter(
                    source_date__day =  courser_day.day).filter(
                    source_date__month =   courser_day.month
                ).count())
            
        
            XAxisList.append(str(courser_day.day))
        

    # mounth < 24 months
    elif(dend-dstart).days < (365 * 2):
        #month year

        get_Month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

        for each in range(0,(dend-dstart).days//30):

            courser_day = dstart + datetime.timedelta(30*each)

            TotalLeadList.append(query.filter(
                    source_date__year =  courser_day.year).filter(
                    source_date__month =   courser_day.month
                ).count())

            NewLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Initial").filter(
                    source_date__year =  courser_day.year).filter(
                    source_date__month =   courser_day.month
                ).count())

            CompletedLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Finish").filter(
                    source_date__year =  courser_day.year).filter(
                    source_date__month =   courser_day.month
                ).count())
        
        
            FolloUpLeadList.append(query.filter(last_lead_activity__lead_status__status_type = "Intermediate").filter(
                    source_date__year =  courser_day.year).filter(
                    source_date__month =   courser_day.month
                ).count())
            
            NonProspectLeadlist.append(query.filter(last_lead_activity__lead_status__status_type = "Negative").filter(
                    source_date__year =  courser_day.year).filter(
                    source_date__month =   courser_day.month
                ).count())
            
        
            XAxisList.append(str(get_Month[courser_day.month % 13 ]))
        

    # year 
    else:
        for each in range(0,((dend-dstart).days)//365):
            # import pdb; pdb.set_trace()
            courser_day = dstart + datetime.timedelta(365*each)

            TotalLeadList.append(query.filter(
                    source_date__year =  courser_day.year
                ).count())

            NewLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Initial").filter(
                    source_date__year =  courser_day.year
                ).count())

            CompletedLeadList.append(
                query.filter(last_lead_activity__lead_status__status_type = "Finish").filter(
                    source_date__year =  courser_day.year
                ).count())
        
        
            FolloUpLeadList.append(query.filter(last_lead_activity__lead_status__status_type = "Intermediate").filter(
                    source_date__year =  courser_day.year
                ).count())
            
            NonProspectLeadlist.append(query.filter(last_lead_activity__lead_status__status_type = "Negative").filter(
                    source_date__year =  courser_day.year
                ).count())
            
        
            XAxisList.append(str(courser_day.year))


    context = {
                "XAxisList" : XAxisList,
                "TotalLeadList":TotalLeadList,
                "NewLeadList":NewLeadList,
                "CompletedLeadList":CompletedLeadList,
                "FolloUpLeadList":FolloUpLeadList,
                "NonProspectLeadlist":NonProspectLeadlist,
                }
    return context

def reportView(request):
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

    # user
    user = CustomUser.objects.get(pk = request.session['userid'])

    if user.builder.id != "FA0001": 
        query = query.filter( builder = user.builder)


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

    # lead_status
    if postRequest.get('agent_list',''):
        query1 = Q()
        for eachprojects in postRequest['agent_list']:
            query1 |= Q(tme__id = eachprojects)
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
        for each in oj.lead_activity.all():
            dataofeachproject = []
            dataofeachproject.append(str(oj.visitor_id))
            dataofeachproject.append(oj.source_date)
            dataofeachproject.append(oj.name)
            dataofeachproject.append(oj.builder.name + ' : <br/>' + oj.project.name)
            dataofeachproject.append(each.user.username if each.user else "None")
            dataofeachproject.append((each.lead_status.name  if each.lead_status else "None") + " : " + (each.call_status.name if  each.call_status else "None") )
            dataofeachproject.append(each.comment.strip() + " : " if each.comment else "None : ")
            Related_Data = (each.telephone.status if each.telephone else "") + " : "
            Related_Data +=  '<audio id="player'+each.telephone.sid+'" src="http://recordings.kookoo.in/livprop/livprop_'+each.telephone.sid+'.mp3"> Your browser does not support </audio><button onclick="document.getElementById(\'player'+each.telephone.sid+'\').play()">Play</button> <button onclick="document.getElementById(\'player'+each.telephone.sid+'\').pause()">Pause</button>'  if each.telephone else "None"
            dataofeachproject.append(Related_Data)
            dataofeachproject.append((each.created + datetime.timedelta(hours=5,minutes=30)).strftime("%I:%M %p %d-%m-%y"))

            listofdata.append(dataofeachproject)

            
        # dataofeachproject = []
        # dataofeachproject.append(str(oj.visitor_id))
        # dataofeachproject.append(oj.source_date)
        # dataofeachproject.append(oj.name)
        # dataofeachproject.append(oj.builder.name + ' : <br/>' + oj.project.name)

        # last_lead_activity_created = ""
        # if oj.last_lead_activity.created:
        #     # last_lead_activity_created += (oj.last_lead_activity.created + datetime.timedelta(0,(60*60*318))).strftime('%I:%M%p %d-%b')
        #     last_lead_activity_created += (oj.last_lead_activity.created).strftime('%I:%M%p %d-%b')
        # else:
        #     last_lead_activity_created += "<br/>"

        # dataofeachproject.append(last_lead_activity_created)

        
        # TME = ""
        # Lead_Status = "" 
        # Call_Status = ""
        # Related_Data = ""
        # count = 0
        # for each in oj.lead_activity.all():
        #     count += 1
        #     TME += str(count) + ") " + (each.user.username + "<hr>" if each.user else "None<hr>")
        #     Lead_Status += str(count) + ") " + (each.lead_status.name  + "<hr>" if each.lead_status else "None<hr>")
        #     Call_Status += str(count) + ") "+ (each.call_status.name  + "<hr>" if  each.call_status else "None<hr>")
        
            
        #     Related_Data += str(count) + ") " + (each.comment.strip() + " : " if each.comment else "None : ")
        #     Related_Data += "At " + (each.next_enquiry_date + datetime.timedelta(hours=5,minutes=30)).strftime("%I:%M %p %d-%m") + " : " if each.next_enquiry_date else "None : "
        #     Related_Data += '<audio id="player'+each.telephone.sid+'" src="http://recordings.kookoo.in/livprop/livprop_'+each.telephone.sid+'.mp3"> Your browser does not support </audio><button onclick="document.getElementById(\'player'+each.telephone.sid+'\').play()">Play</button> <button onclick="document.getElementById(\'player'+each.telephone.sid+'\').pause()">Pause</button><hr>'  if each.telephone else "None<hr>"
            
            


            # addr = ""  
            # if each.remote_addr:
            #     addr = each.remote_addr
            # else:
            #     addr += "None<hr>" 
            # mail = ""
            # if each.remote_addr:
            #     mail = each.remote_addr
            # else:
            #     mail += "None<hr>"

          

            # relateddata += next_enquiry_date + ": <a href='#' title='details' onclick=\"details('"+comment+"','"+sid+"','"+addr+"','"+mail+"')\">Details</a><hr>"

            # createddate += each.created.strftime('%I:%M%p %d-%b') + "<hr>" 

        # else:
        #     lead_status += "<br/>"


        # if oj.last_lead_activity.call_status:
        #     call_status += oj.last_lead_activity.comment
        # else:
        #     lead_status += "<br/>"


        # dataofeachproject.append(TME)
        # dataofeachproject.append(Call_Status)
        # dataofeachproject.append(Lead_Status)
        # dataofeachproject.append(Related_Data)
      
        # dataofeachproject.append('call_status')

        # dataofeachproject.append("relateddata")
        
        

        # tme = ""
        # if oj.tme:
        #     tme = oj.tme.username
        # dataofeachproject.append(tme)
        
        # chat 
        # dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Click</button>")
       


    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }

    return context

def agents_activityView(request):
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

  
    # user
    user = CustomUser.objects.get(pk = request.session['userid'])

    if user.builder.id != "FA0001": 
        query = query.filter( builder = user.builder)


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

    # lead_status
    if postRequest.get('agent_list',''):
        query1 = Q()
        for eachprojects in postRequest['agent_list']:
            query1 |= Q(tme__id = eachprojects)
        query = query.filter(query1)

    if request.POST['search']:
        query1 = Q()
        query1 |= Q(pk = postRequest['search'][0])
        # query1 |= Q(visitor_id__icontains = postRequest['search'][0])
        query1 |= Q(name__icontains = postRequest['search'][0])
        query = query.filter(query1)

    # import pdb; pdb.set_trace()

    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    dataofeachproject = ['visitor_id','source_date','name']

    if request.POST['orderDir'] == "desc":
        query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    else:
        query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])


    query = query.order_by('last_lead_activity__created')

    # query = query.order_by('modified')

    query = query[start:stop]

    for oj in query:
        dataofeachproject = []
        dataofeachproject.append(str(oj.id))
        dataofeachproject.append(oj.source_date)
        dataofeachproject.append(str(oj.visitor_id))
        dataofeachproject.append(oj.name)
        dataofeachproject.append(oj.builder.name + '<br/>' + oj.project.name)

       
        lead_status = ""
        if oj.last_lead_activity.lead_status:
            lead_status += oj.last_lead_activity.lead_status.name + "<br/>" 
        else:
            lead_status += "<br/>"
        dataofeachproject.append( lead_status)

        call_status = ""        
        if oj.last_lead_activity.call_status:
            call_status += oj.last_lead_activity.call_status.name + "<br/>" 
            call_status += oj.last_lead_activity.comment
        else:
            lead_status += "<br/>"
        dataofeachproject.append(call_status)
        
       
        

        tme = ""
        if oj.tme:
            tme = oj.tme.username
        dataofeachproject.append(tme)
       
        dataofeachproject.append((oj.modified + datetime.timedelta(hours=5,minutes=30)).strftime('%a, %d-%b-%y %I:%M:%S %p'))


        if  oj.last_lead_activity.telephone:
            sid = oj.last_lead_activity.telephone.status + " : <audio id='player"+oj.last_lead_activity.telephone.sid+"' src='http://recordings.kookoo.in/livprop/livprop_"+ oj.last_lead_activity.telephone.sid+".mp3'></audio> <button onclick='document.getElementById(\"player"+oj.last_lead_activity.telephone.sid+"\").play()'>Play</button> <button onclick='document.getElementById(\"player"+oj.last_lead_activity.telephone.sid+"\").pause()'>Pause</button>"
                        
        else:
            sid = "None<hr>" 

        dataofeachproject.append(sid)
        
        # chat 
        # dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Click</button>")
       


        listofdata.append(dataofeachproject)
    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }

    return context

def Lead_assignViews(request):
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

  
    # user
    user = CustomUser.objects.get(pk = request.session['userid'])

    if user.builder.id != "FA0001": 
        query = query.filter( builder = user.builder)


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

    # lead_status
    if postRequest.get('agent_list',''):
        query1 = Q()
        for eachprojects in postRequest['agent_list']:
            query1 |= Q(tme__id = eachprojects)
        query = query.filter(query1)

    if request.POST['search']:
        query1 = Q()
        query1 |= Q(visitor_id__icontains = postRequest['search'][0])
        query1 |= Q(name__icontains = postRequest['search'][0])
        query = query.filter(query1)

    # import pdb; pdb.set_trace()

    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    dataofeachproject = ['visitor_id','source_date','name']

    if request.POST['orderDir'] == "desc":
        query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    else:
        query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])


    query = query.order_by('last_lead_activity__created')

    # query = query.order_by('modified')

    query = query[start:stop]

    for oj in query:
        dataofeachproject = []
        dataofeachproject.append(str(oj.id))
        dataofeachproject.append(oj.source_date)
        dataofeachproject.append(str(oj.visitor_id))
        dataofeachproject.append(oj.name)
        dataofeachproject.append(oj.builder.name + '<br/>' + oj.project.name)

       
        lead_status = ""
        if oj.last_lead_activity.lead_status:
            lead_status += oj.last_lead_activity.lead_status.name + "<br/>" 
        else:
            lead_status += "<br/>"
        dataofeachproject.append( lead_status)

        call_status = ""        
        if oj.last_lead_activity.call_status:
            call_status += oj.last_lead_activity.call_status.name + "<br/>" 
            call_status += oj.last_lead_activity.comment
        else:
            lead_status += "<br/>"
        dataofeachproject.append(call_status)
        
        # dataofeachproject.append(oj.status_error)

        tme = ""
        if oj.tme:
            tme = oj.tme.username
        dataofeachproject.append(tme)
        
             
        

        select = '<select  id="reassign_tele_id" name="reassign_tele_id" class="form-control"><option value="">Select</option>'
        
        for eachagent in CustomUser.objects.filter(user_roles__user_type = 'FT'):
            select += '<option value="' + str(eachagent.pk) + '">' + eachagent.username + '</option>'
        
        select += '</select><div class="error">Can not be empty</div>'
        dataofeachproject.append(select)
        # dataofeachproject.append("<button title='Edit' type='button'  data-id='"+str(oj.id)+"'  class='btn btn-outline btn-primary edit-lead' onclick='Assign("+str(oj.pk)+")'>Assign</button>")


        # dataofeachproject.append("<select id='reassign_tele_id' name='reassign_tele_id' class='form-control'><option value=''>Select</option>"+ stringselect +"</select><div class='error'>Can not be empty</div>")
        selectstatus="<button type='button' class='btn btn-primary' data-id='"+str(oj.id)+"' value='Assign' onclick='assigntme(this)'>Assign</button>"
        dataofeachproject.append(selectstatus)


        # dataofeachproject.append('')
        
        # chat 
       


        listofdata.append(dataofeachproject)
    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }

    return context

def Lead_assign_saveViews(request):
    id = request.POST.get('id','')
    tme = request.POST.get('tme','')
    user = CustomUser.objects.get(id=tme)
    lead = Lead.objects.get(id = id)
    lead_activity1 = LeadActivity.objects.create(
                activity_type = 'other',
                remote_addr = request.META['REMOTE_ADDR'],
                remote_url_requested = request.META['HTTP_REFERER'],
                user =  CustomUser.objects.get(pk = request.session['userid']),
                comment = user.username + "(TME Agent) is reassign manualy by " + CustomUser.objects.get(pk = request.session['userid']).username
            )
    lead.lead_activity.add(lead_activity1)
    lead.tme = user
    lead.save()
    context = {}
    return context

def live_chatsView(request):
    listofdata = []
    postRequest = dict(request.POST)

    query = Q()
    # date
    if postRequest['startdate'][0] and postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        dateend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = APIRequestLog.objects.filter(requested_at__gte = datestart).filter(requested_at__lte = dateend)

    elif postRequest['startdate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        query = APIRequestLog.objects.filter(requested_at = datestart)

    elif postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = APIRequestLog.objects.filter(requested_at = datestart)

    else:
        query = APIRequestLog.objects.all()

 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query.order_by('requested_at')
    query = query[start:stop]


    for oj in query:
        dataofeachproject = []

        
        dataofeachproject.append(oj.id)
        dataofeachproject.append((oj.requested_at + datetime.timedelta(hours=5,minutes=30)).strftime('%a, %d-%b-%y %I:%M:%S %p'))
        dataofeachproject.append(oj.response_ms)
        dataofeachproject.append(oj.path)
        dataofeachproject.append(oj.remote_addr)
        dataofeachproject.append(oj.host)
        dataofeachproject.append(oj.response if False else "")
        dataofeachproject.append(oj.status_code)
        dataofeachproject.append(oj.errors)






        # header = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']

        # for each in header:
        #     dataofeachproject.append(getattr(oj,each))

        listofdata.append(dataofeachproject)
    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context


def cronView(request):
    listofdata = []
    postRequest = dict(request.POST)

    query = Q()
    # date
    if postRequest['startdate'][0] and postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        dateend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = CronJobLog.objects.filter(start_time__gte = datestart).filter(start_time__lte = dateend)

    elif postRequest['startdate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        query = CronJobLog.objects.filter(start_time = datestart)

    elif postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = CronJobLog.objects.filter(start_time = datestart)

    else:
        query = CronJobLog.objects.all()

 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query.order_by('start_time')
    query = query[start:stop]


    for oj in query:
        dataofeachproject = []


        dataofeachproject.append(oj.id)
        dataofeachproject.append((oj.start_time + datetime.timedelta(hours=5,minutes=30)).strftime('%a, %d-%b-%y %I:%M:%S %p'))
        dataofeachproject.append((oj.end_time + datetime.timedelta(hours=5,minutes=30)).strftime('%a, %d-%b-%y %I:%M:%S %p'))
        dataofeachproject.append(oj.message)
        dataofeachproject.append(oj.ran_at_time)
        dataofeachproject.append(oj.is_success)






        # header = ['lead','user','requested_at','response_ms','path','remote_addr','host','query_params','response','status_code','errors']

        # for each in header:
        #     dataofeachproject.append(getattr(oj,each))

        listofdata.append(dataofeachproject)
    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context



def emailsViews(request):
    listofdata = []
    postRequest = dict(request.POST)

    query = Q()
    # date
    if postRequest['startdate'][0] and postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        dateend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = Emailaddress.objects.filter(created__gte = datestart).filter(created__lte = dateend)

    elif postRequest['startdate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        query = Emailaddress.objects.filter(created = datestart)

    elif postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = Emailaddress.objects.filter(created = datestart)

    else:
        query = Emailaddress.objects.all()

 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query.order_by('created')
    query = query[start:stop]


    for oj in query:
        dataofeachproject = []
        dataofeachproject.append(oj.id)
        dataofeachproject.append(str_decode(oj.mail_id))
        dataofeachproject.append(oj.builder.name)
        dataofeachproject.append(oj.status_error)
        dataofeachproject.append(oj.created.strftime('%a, %d-%b-%y %I:%M:%S %p'))
        dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Edit</button>")

        listofdata.append(dataofeachproject)

    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context



def phoneViews(request):
    listofdata = []
    postRequest = dict(request.POST)

    query = Q()
    # date
    if postRequest['startdate'][0] and postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        dateend = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = PhoneNumber.objects.filter(created__gte = datestart).filter(created__lte = dateend)

    elif postRequest['startdate'][0]:
        datestart = datetime.datetime.strptime(postRequest['startdate'][0], "%d/%m/%Y").date()
        query = PhoneNumber.objects.filter(created = datestart)

    elif postRequest['enddate'][0]:
        datestart = datetime.datetime.strptime(postRequest['enddate'][0], "%d/%m/%Y").date()
        query = PhoneNumber.objects.filter(created = datestart)

    else:
        query = PhoneNumber.objects.all()

 
    if request.POST['search']:
        query1 = Q()
        query1 |= Q(id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
        query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query.order_by('created')
    query = query[start:stop]


    for oj in query:
        dataofeachproject = []
        dataofeachproject.append(oj.id)
        dataofeachproject.append(str_decode(oj.number))
        dataofeachproject.append(oj.builder.name)
        dataofeachproject.append(oj.status_error)
        dataofeachproject.append(oj.created.strftime('%a, %d-%b-%y %I:%M:%S %p'))
        # dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Edit</button>")
        dataofeachproject.append("")

        listofdata.append(dataofeachproject)

    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context


def UserViews(request):
    listofdata = []
    postRequest = dict(request.POST)
    localuser=CustomUser.objects.get(pk=request.session['userid'])
    query = Q()
  
    query = CustomUser.objects.filter(builder=localuser.builder).exclude(id=localuser.id).exclude(username="root")

 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query[start:stop]


    for oj in query:
        dataofeachproject = []
        dataofeachproject.append(oj.id)
        dataofeachproject.append(oj.username)
        dataofeachproject.append(oj.first_name)
        dataofeachproject.append(oj.last_name)
        dataofeachproject.append(oj.phone)
        dataofeachproject.append(oj.email)
        dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='edit(\"users\","+str(oj.pk)+")'>Edit</button>")
        listofdata.append(dataofeachproject)

    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context


def buildersViews(request):
    listofdata = []
    postRequest = dict(request.POST)
    localuser=CustomUser.objects.get(pk=request.session['userid'])
    query = Q()
  
    query = Builder.objects.all()
    # 
 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query[start:stop]


    for oj in query:
        dataofeachproject = []

        dataofeachproject.append(oj.id)
        dataofeachproject.append(oj.name)
        dataofeachproject.append(oj.package.name)
        dataofeachproject.append(oj.limit_reached)
        dataofeachproject.append(oj.start_date)
        dataofeachproject.append(oj.is_livprop_tranfer)
        dataofeachproject.append(oj.is_encryption)
        dataofeachproject.append(oj.is_auto_assign_tme)
        dataofeachproject.append(oj.service.name)
        dataofeachproject.append(oj.is_active)
        dataofeachproject.append(oj.created.strftime('%a, %d-%b-%y %I:%M:%S %p'))

        dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Edit</button>")
        listofdata.append(dataofeachproject)

    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context


def buildersApiViews(request):
    listofdata = []
    postRequest = dict(request.POST)
    localuser=CustomUser.objects.get(pk=request.session['userid'])
    query = Q()
  
    query = Builder.objects.all()
    # 
 
    # if request.POST['search']:
    #     query1 = Q()
    #     query1 |= Q(visitor_id__icontains = postRequest['search'][0])
    #     query1 |= Q(name__icontains = postRequest['search'][0])
    #     query = query.filter(query1)


    recordsTotal = query.count()

    start = int(postRequest['start'][0])
    stop = int(postRequest['length'][0]) + int(postRequest['start'][0])

    # dataofeachproject = ['visitor_id','source_date','name']

    # if request.POST['orderDir'] == "desc":
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1]).reverse()
    # else:
    #     query = query.order_by(dataofeachproject[int(postRequest['orderCol'][0])-1])

    query = query[start:stop]


    for oj in query:
        dataofeachproject = []

        dataofeachproject.append(oj.id)
        dataofeachproject.append(oj.name)
        dataofeachproject.append(oj.package.name)
        dataofeachproject.append(oj.limit_reached)
        dataofeachproject.append(oj.start_date)
        dataofeachproject.append(oj.is_livprop_tranfer)
        dataofeachproject.append(oj.is_encryption)
        dataofeachproject.append(oj.is_auto_assign_tme)
        dataofeachproject.append(oj.service.name)
        dataofeachproject.append(oj.is_active)
        dataofeachproject.append(oj.created)

        dataofeachproject.append("<button title='Edit' type='button' class='btn btn-outline btn-primary edit-lead' onclick='Chat("+str(oj.pk)+")'>Edit</button>")
        listofdata.append(dataofeachproject)

    context = {
    "aaData":listofdata,
    "recordsTotal":recordsTotal,
    "recordsFiltered":recordsTotal,
    }
    return context