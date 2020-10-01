# import json
# from management.models import *
# from .models import *
# from django.db.models import Q

# def notifcationRefresh(userid):
#     # info
#     query = Q()
#     query = Lead.objects.filter(flags__tme = userid)
#     AllTotalCount = query.count()
#     AllFollowp = query.filter(flags__last_lead_activity_lead_status__status_type = "Intermediate")
#     AllComplited = query.filter(flags__last_lead_activity_lead_status__status_type = "Finish")

#     query1 = query.filter() 
#     MonthTotalCount = query1.count()
#     MonthFollowp = query1.filter(flags__last_lead_activity_lead_status__status_type = "Intermediate")
#     MonthComplited = query1.filter(flags__last_lead_activity_lead_status__status_type = "Finish")
    
#     query2 = query.filter() 
#     WeekTotalCount =  query2.count()
#     WeekFollowp = query2.filter(flags__last_lead_activity_lead_status__status_type = "Intermediate")
#     WeekComplited = query2.filter(flags__last_lead_activity_lead_status__status_type = "Finish")

#     query3 = query.filter() 
#     dayTotalCount =  query3.count()
#     dayFollowp = query3.filter(flags__last_lead_activity_lead_status__status_type = "Intermediate")
#     dayComplited = query3.filter(flags__last_lead_activity_lead_status__status_type = "Finish")

#     info = {
#         "D":{
#             "f":dayFollowp,
#             "c":dayComplited,
#             "t":dayTotalCount,
#         },
#         "W":{
#             "f":WeekFollowp,
#             "c":WeekComplited,
#             "t":WeekTotalCount,
#         },
#         "M":{
#             "f":MonthFollowp,
#             "c":MonthComplited,
#             "t":MonthTotalCount,
#         },
#         "A":{
#             "f":AllFollowp,
#             "c":AllComplited,
#             "t":AllTotalCount,
#         }
#     }


#     # notification
#     query4 = query.filter(flags__last_lead_activity_lead_status__status_type = 'Initial') 
#     notification = {
#         "Mi":"",
#         "Nc":query4.count()
#     }

#     # alert
#     LeadList = []

#     for each in :
#         leadeach = {
#             "id":each.pk,
#             "Na":each.name,
#             "Ls":each.flags.last_lead_activity_lead_status.name,
#             "ti":
#             "Go":
#         }
#         LeadList.append(leadeach)
    
#     alert = {
#         "Ll":LeadList
#     }

#     # incomingalert
#     incomingalert = {
#         "id":"",
#         "Na":"",
#         "Cs":"",
#         "Ls":"",
#         "ti":""
#     }

#     context = {
#         "info":info,
#         "notification":notification,
#         "alert":alert,
#         "incomingalert":incomingalert
#     }

#     notifcation = Notifcation.objects.filter(user=userid)
#     if len(notifcation) == 0:
#         notifcation = Notifcation.objects.create(
#             user = userid,
#             data = json.dumps(context) 
#         )
#     else:
#         notifcation[0].data = json.dumps(context) 



    