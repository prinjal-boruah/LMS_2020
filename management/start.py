



from management.models import *
from inbound.models import *
from dashboard.models import *

import datetime


def createNewInstance():
    package = Package.objects.filter(name='default')
    if len(package) == 0:
        print('creating tables ')

        package = Package.objects.create(
            name = 'default',
            tme_limit = 5,
            bd_limit = 5,
            tmebd_limit = 5,
            is_auto_assign_tme = True,
            is_auto_assign_bd = True

        )


        Site_Visit_list = []

        leadstatus = LeadStatus.objects.create(
            name = 'None'
        ) 
        Site_Visit_list.append(leadstatus)



        leadstatus = LeadStatus.objects.create(
            name = 'Site Visit completed',
            status_type = 'Finish'
        ) 
        Site_Visit_list.append(leadstatus)




        leadstatus = LeadStatus.objects.create(
            name = 'Scheduled for Site visit',
            status_type = 'Intermediate'
        ) 
        Site_Visit_list.append(leadstatus)



        leadstatus = LeadStatus.objects.create(
            name = 'Intersted For Site Visit',
            status_type = 'Intermediate'
        ) 
        Site_Visit_list.append(leadstatus)



        leadstatus = LeadStatus.objects.create(
            name = 'Not Intersted',
            status_type = 'Negative'
        ) 
        Site_Visit_list.append(leadstatus)




        leadstatus = LeadStatus.objects.create(
            name = 'Follow up',
            status_type = 'Intermediate'
        ) 
        Site_Visit_list.append(leadstatus)



        leadstatus = LeadStatus.objects.create(
            name = 'Already visited Site',
            status_type = 'Negative'
        ) 
        Site_Visit_list.append(leadstatus)


        leadstatus = LeadStatus.objects.create(
            name = 'Invalid Contact',
            status_type = 'Negative'
        ) 
        Site_Visit_list.append(leadstatus)


        service = Service.objects.create(
            name = 'Site Visit'
        )

        service.status.add(*Site_Visit_list)
        service.save()





        Lead_Validated_list = []

        leadstatus = LeadStatus.objects.create(
            name = 'Lead Validated',
            status_type = 'Finish'
        ) 
        Lead_Validated_list.append(leadstatus)


        leadstatus = LeadStatus.objects.create(
            name = 'Follow up',
            status_type = 'Intermediate'
        ) 
        Lead_Validated_list.append(leadstatus)

        service = Service.objects.create(
            name = 'Lead Validated'
        )

        service.status.add(*Lead_Validated_list)
        service.save()



        # fulfilment
        Builder.objects.create(
            id = '00000',
            name = 'fulfilment',
            package = package,
            start_date = datetime.datetime.now().date(),
            is_auto_assign_tme = True,
            is_auto_assign_bd = True,
            service = service,
        ) 


        role0 = UserRole.objects.create(
            name = 'Super Admin',
            ui_type = 'MA',
            user_type = 'CT'
        )


        role1 = UserRole.objects.create(
            name = 'Client TME',
            ui_type = 'ED',
            user_type = 'CT'
        )

        role2 = UserRole.objects.create(
            name = 'Fullfilment TME',
            ui_type = 'ED',
            user_type = 'FT'
        )

        role3 = UserRole.objects.create(
            name = 'Fullfilment Admin',
            ui_type = 'MA',
            user_type = 'FA'
        )

        role4 = UserRole.objects.create(
            name = 'Client Admin',
            ui_type = 'CA',
            user_type = 'FA'
        )

        user = CustomUser(
        is_superuser = True,
        username = 'root',
        first_name = 'SupeAdmin',
        last_name  = '',
        email = 'admin@livserv.com',
        is_staff = True,
        is_active = True,
        builder_id ='00000',
        user_roles_id= 1
        )
        user.set_password('anand123')
        user.save()


        # user = CustomUser( 
        #     is_superuser = False, 
        #     username = 'FTME',
        #     first_name = 'FTME',
        #     last_name  = '',
        #     email = 'admin@livserv.com',
        #     is_staff = True,
        #     is_active = True,
        #     builder_id = '00000', 
        #     user_roles_id= 3
        #     )
        # user.set_password('anand123')
        # user.save()





        callstatus = CallStatus.objects.create(
            name = 'None'
        ) 
        

        callstatus = CallStatus.objects.create(
            name = 'Completed',
            status_type = 'Finish'
        ) 
        

        callstatus = CallStatus.objects.create(
            name = 'Ringing Not respond',
            status_type = 'Intermediate'
        ) 
        


        callstatus = CallStatus.objects.create(
            name = 'Call Back',
            status_type = 'Intermediate'
        ) 
        

        callstatus = CallStatus.objects.create(
            name = 'Incoming call',
            status_type = 'Intermediate'
        ) 
        

        callstatus = CallStatus.objects.create(
            name = 'International Call',
            status_type = 'Negative'
        ) 
        



        callstatus = CallStatus.objects.create(
            name = 'Wrong Number',
            status_type = 'Negative'
        ) 
        


        callstatus = CallStatus.objects.create(
            name = 'Contact Not shared',
            status_type = 'Negative'
        ) 
        























# CustomUser.create( is_superuser = False, username = 'FTME',first_name = 'FTME',last_name  = '',email = 'admin@livserv.com',is_staff = True,is_active = True,builder_id = '00000', user_roles_id= 3)

