
import email
import logging
import numbers
from builtins import IndexError, ValueError, object

from management.models import *
from rest_framework import serializers
from management.customencryption import *

logger = logging.getLogger(__name__)
import sys

from .models import *

from datetime import timedelta 
import datetime

class livechatleadSerializer(serializers.ModelSerializer):

    # compid = serializers.IntegerField(source='builder.id')
    # cmpname = serializers.CharField(source='builder.name')
    # propid = serializers.IntegerField(source='project.id')
    # property = serializers.CharField(source='project.name')
    # visemail = serializers.CharField(source='email.mail_id', write_only=True,required=False)
    # visphone = serializers.CharField(source='phone.number', write_only=True,required=False)
    # leadDate = serializers.CharField(source='source_date')
    # customerName = serializers.CharField(source='name',required=False)
    # country = serializers.CharField(source='country.name',required=False)
    # city = serializers.CharField(source='city.name',required=False)
    # chVisitid = serializers.CharField(source='visitor_id')
    # fldrname = serializers.CharField(source='live_chat.folder', write_only=True)
    # serverid = serializers.CharField(source='live_chat.server_id', write_only=True)
    # websiteurl = serializers.CharField(source='live_chat.web_site_url',write_only=True,required=False)
    # additional = serializers.CharField(source='live_chat.additional',write_only=True,required=False)
    # source = serializers.CharField(source='live_chat.source',write_only=True,required=False)
    

    class Meta:
        model = APILead
        fields = '__all__'
        # fields = ( 
        #            'chVisitid',
        #            'compid', 'cmpname', 
        #            'propid', 'property',
        #            'visemail', 'visphone',
        #            'leadDate',
        #            'customerName',
        #            'country', 'city',
        #            'fldrname','serverid',
        #            'websiteurl','additional','source'
        # )

    

    # def create(self,validated_data):
        
        # '''
        # Todo list
        # #/    builder (check and create)
        # #/    project (check and create)
        # #/    mail  (check and create)
        # #/    phone  (check and create)
        # #/    country  (check and create)
        # #/    city  (check and create)
        # #/    chat  (check and create)

        # '''


        
        # if not((validated_data.get('phone','')) or (validated_data.get('email',''))):
        #     raise serializers.ValidationError('At least one phone number or email id is required')
        
        

        # # creation started
        
        
        # builder_model, builder_created_flag = Builder.objects.update_or_create(
        #     id =  validated_data['builder']['id']
        # )   
        # builder_model.name = validated_data['builder']['name']
        # builder_model.save()

      
        
        
        # project_model, project_created_flag  = Project.objects.update_or_create(
        #     id =  validated_data['project']['id']
        # )
        # project_model.name =  validated_data['project']['name']
        # project_model.builder = builder_model
        # project_model.save()




        # country_model, country_created_flag  = Country.objects.update_or_create(
        #      name =  validated_data['country']['name']
        # )
        # country_model.save()


        # city_model, city_created_flag  = City.objects.update_or_create(
        #     name =  validated_data['city']['name']
        # )
        # city_model.save()
    

        # web_site_url_model, web_site_url_created_flag  = WebSiteUrl.objects.update_or_create(
        #     name =  validated_data['live_chat']['web_site_url']
        # )
        # web_site_url_model.save()

        
        # source_model, source_created_flag  = Source.objects.update_or_create(
        #     name =  validated_data['live_chat']['source']
        # )
        # source_model.save()


        # folder_model, folder_created_flag  = Folder.objects.update_or_create(
        #     name =  validated_data['live_chat']['folder']
        # )
        # folder_model.save()
          
        # server_id_model, server_id_created_flag  = ServerId.objects.update_or_create(
        #     name =  validated_data['live_chat']['server_id']
        # )
        # server_id_model.save()

          
        
        # '''
        # Checks lead repeated or not
        # It checks depends on
        # same builder, phone,
        # email id
        # ''' 

        # check_repeated_phone = None
        # check_repeated_mail = None


        # if (validated_data.get('phone','')):
        #     phone_numbers = validated_data['phone']['number'].split(',')
        #     for each in phone_numbers:
        #         encrypted_phone = str_encode(each,True)
        #         try:
        #             check_repeated_phone = PhoneNumber.objects.filter(
        #                                                         builder=builder_model
        #                                                        ).get(
        #                                                         number=encrypted_phone
        #                                                        )
        #             repeated_lead = Lead.objects.get(
        #                                             phone=check_repeated_phone
        #                                             )
        #         except PhoneNumber.DoesNotExist:
        #             check_repeated_phone = None


        # elif (validated_data.get('email','')):
        #     mail_ids = validated_data['email']['mail_id'].split(',')
        #     for each in mail_ids:
        #         encrypted_email = str_encode(each,False)
        #         try:
        #             check_repeated_mail = Email.objects.filter(
        #                                                         builder=builder_model
        #                                                     ).get(
        #                                                         mail_id=encrypted_email
        #                                                     )
        #             repeated_lead = Lead.objects.get(
        #                                             phone=check_repeated_mail
        #                                             )
        #         except Email.DoesNotExist:
        #             check_repeated_mail = None

      



        # # repeated check phone and mail
        # if check_repeated_phone != None or check_repeated_mail != None:
        #     pass
            
         


        
        # # repeated check not repeated lead
        # else:
        #     # m
        #     if validated_data.get('phone',''):
        #         phone_numbers = validated_data['phone']['number'].split(',')
        #         phone_models = []
        #         for each in phone_numbers:
        #             encrypted_phone = str_encode(each,True)
        #             phone_model = PhoneNumber(
        #                                         builder=builder_model,
        #                                         number=encrypted_phone
        #                                     )
        #             phone_model.save()
        #             phone_models.append(phone_model)
        #     else:
        #         phone_models = []

        #     # m
        #     if validated_data.get('email',''):
        #         mail_ids = validated_data['email']['mail_id'].split(',')
        #         mail_models = []
        #         for each in mail_ids:
        #             encrypted_email = str_encode(each,False)    

        #             mail_model = Email(
        #                                 builder=builder_model,
        #                                 mail_id=encrypted_email
        #                             )
        #             mail_model.save()
        #             mail_models.append(mail_model)
                
        #     else:
        #         mail_models = []



        #     live_chat_model = LiveChat(
        #         web_site_url = web_site_url_model,
        #         source = source_model,
        #         folder = folder_model,
        #         server_id = server_id_model,
        #         additional = validated_data['live_chat']['additional']
                
        #     )
        #     live_chat_model.save()

        #     lead = Lead(
        #             visitor_id =  validated_data['visitor_id'],
        #             source_date =  validated_data['source_date'],
        #             name =  validated_data['name'],
        #             country = country_model,
        #             city = city_model,
        #             builder = builder_model,
        #             project = project_model,       
                    
        #     )
    
    
            
        #     # chat_url genration 
        #     try:
        #         live_chat_model.chat_url = (
        #                 'http:/{server_id}/livserv/viewchat/chatMsg4clientTasklist.jsp?chVisitid={visitor_id}&comcode={folder}&yea={source_date}'.format(
        #                     server_id = source_model.name ,
        #                     visitor_id = lead.visitor_id,
        #                     folder = folder_model.name,
        #                     source_date = '-'.join(lead.source_date.split('-')[:3])
        #                     ))
        #         live_chat_model.save()
        #     except:
        #         logger.exception('Logging chat_url raise exception! : {}'.format(sys.exc_info()[0]))

        #     lead.save()


        #     if len(phone_models) > 0:
        #         lead.phone.add(*phone_models)
            
        #     if len(mail_models) > 0:
        #         lead.email.add(*mail_models)
            
        #     lead.live_chat.add(live_chat_model)
            

        #     # add the LeadActivity 

        #     request = self.context['request']
        #     ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        #     if ipaddr:
        #         ipaddr =  ipaddr.split(",")[0].strip()
        #     ipaddr = request.META.get("REMOTE_ADDR", "")
       

            
            

        #     fieldsChangeds = []
        #     for each in self.data:
        #         fieldsChanged = FielsChanged(
        #             feilds = each,
        #             old_data = '' ,
        #             new_data = self.data[each]
        #             )
        #         fieldsChanged.save()
        #         fieldsChangeds.append(fieldsChanged)



        #     fiels_to_other = [
        #         'folder',
        #         'server_id',
        #         'web_site_url',
        #         'additional',
        #         'source',
        #     ]

        #     for each in fiels_to_other:
        #         fieldsChanged = FielsChanged(
        #             feilds = each,
        #             old_data = '' ,
        #             new_data = validated_data['live_chat'][each]
        #             )
        #         fieldsChanged.save()
        #         fieldsChangeds.append(fieldsChanged)



        #     if validated_data.get('email',''):

        #         fieldsChanged = FielsChanged(
        #                 feilds = each,
        #                 old_data = '' ,
        #                 new_data = validated_data['email']['mail_id']
        #                 )
        #         fieldsChanged.save()
        #         fieldsChangeds.append(fieldsChanged)
            

        #     if validated_data.get('phone',''):
        #         fieldsChanged = FielsChanged(
        #                 feilds = each,
        #                 old_data = '' ,
        #                 new_data = validated_data['phone']['number']
        #                 )
        #         fieldsChanged.save()
        #         fieldsChangeds.append(fieldsChanged)

    

        #     lead_activity = LeadActivity(
        #         activity_type = 'system',
        #         remote_addr = ipaddr,
        #         remote_url_requested = request.get_host()
        #         )

        #     lead_activity.save()

        #     if len(fieldsChangeds) > 0:
        #         lead_activity.fiels_changed.add(*fieldsChangeds)



        #     # # Todo need to Tranfer the lead to the Agent 
        #     # # import pdb;pdb.set_trace()


        #     # # testing purpose value changed 
        #     # builder_model.is_auto_assign_tme = True
        #     # builder_model.save()




        #     # main code
        #     if builder_model.is_active and builder_model.is_auto_assign_tme:
        #         if builder_model.package == '':
        #             if len(Package.objects.all()) > 0:
        #                 package = Package(
        #                         name = 'Default',    
        #                         tme_limit = 100,                                
        #                         bd_limit = 100,                                
        #                         tmebd_limit = 100,
        #                         is_auto_assign_tme = True,
        #                         is_auto_assign_bd = True
        #                     )
        #                 package.save()
        #             else:
        #                 package = Package.objects.get(name='Default')
                    
                    
        #             builder_model.add(package)

        #         # expery date 
        #         lastday = timedelta(days=int(builder_model.package.validity_days))

        #         if ((builder_model.start_date + lastday) > datetime.datetime.now().date()):


        #             if builder_model.limit_reached < builder_model.package.lead_limit: 
                        


        #                 # import pdb ; pdb.set_trace()
        #                 try:
        #                     builderAutoAssignInfo = BuilderAutoAssignInfo.objects.get(builder=builder_model)
                            
        #                 except BuilderAutoAssignInfo.DoesNotExist:
        #                     builderAutoAssignInfo = BuilderAutoAssignInfo(
        #                         builder=builder_model,
        #                     )
        #                     builderAutoAssignInfo.save()


        #                 # agent list fetching  
        #                 if builder_model.is_livprop_tranfer:

        #                     agents_list = CustomUser.objects.filter(
        #                         user_roles__user_type = 'FT'
        #                         ).filter(
        #                             is_active = True
        #                         ).order_by('pk')
                           
        #                 else:
                        
        #                     agents_list = CustomUser.objects.filter(
        #                         user_roles__user_type = 'CT'
        #                         ).filter(
        #                             is_active = True
        #                         ).order_by('pk')


        #                 if not agents_list:
        #                     logger.exception('agent are not found')
                        

        #                 else:
        #                     # last assiged
        #                     if builderAutoAssignInfo.last_tme:
        #                         last_agent = builderAutoAssignInfo.last_tme # old is already assigied 
        #                     else:
        #                         last_agent = agents_list[len(agents_list)-1] #if last assigned is null 


        #                     # avilabitly  
        #                     agents_list_pk =  list(map(lambda agents_list: agents_list.pk,agents_list))
                            
        #                     agentAvilable = AgentAvailability.objects.filter(
        #                             agent__pk__in = agents_list_pk
        #                         ).filter(
        #                             upto__gt = datetime.datetime.now()
        #                         )


        #                     # priority
        #                     agentpriority = LeadAssignPriority.objects.filter(
        #                             agent__pk__in = agents_list_pk
        #                         ).filter(
        #                             upto__gt = datetime.datetime.now()
        #                         )



        #                     # last assign agent in list 

        #                     index = 0
        #                     for key,each in enumerate(agents_list):
        #                         if each.id == last_agent.id:
        #                             index = key
                    

        #                     index2 = index
                            
        #                     # index 
        #                     while True:
 
                                
        #                         if agents_list[index] in agentAvilable:  
        #                             continue                      
                                
        #                         else:
        #                             if agents_list[index] in agentpriority:
                                        
        #                                 agentB = agentpriority.index(agents_list[index])
        #                                 if agentpriority[agentB].projects == project_model:
        #                                     agenttoassign = agentpriority[agentB]
        #                                     break
                       
        #                         index = (index + 1) % len(agents_list) 
                                
        #                         if index == index2:
        #                             agenttoassign = agents_list[index]
        #                             break

                           
        #                     # updating   
        #                     if not agenttoassign:
        #                         agenttoassign  = agents_list[index2+1]
                            

        #                     flags = LeadFlags(
        #                         tme = agenttoassign
        #                     )
        #                     flags.save()
        #                     lead.flags = flags
        #                     lead.save()

        #                     builderAutoAssignInfo.last_tme = agenttoassign
        #                     builderAutoAssignInfo.save()
                            


        #             else:
        #                 logger.exception('builder lead limit')

                        
        #         else:
        #             logger.exception('builder date epired')

        #     return lead



# class LeadAssignPriority(models.Model):

#     agent = models.ForeignKey(CustomUser,related_name='agentL',on_delete=models.CASCADE)
    
#     upto = models.DateTimeField(auto_now=True)

#     projects = models.ManyToManyField(Project,db_column='Fiels Changed',blank=True)

#     who_updated = models.ForeignKey(CustomUser,related_name='who_updatedL',on_delete=models.CASCADE)

#     created = models.DateTimeField(auto_now=False, auto_now_add=True)

#     def __str__(self):
#         return str(self.pk)