from management.models import *
import datetime
import re
import phonenumbers
from management.customencryption import *
# from string import punctuation
# from management.customencryption import *

def find_models(eachlead):

    country_model,city_model,websiteurl,source,fldrname,serverid = ('','','','','','')

    # builder
    builder_model, builder_created_flag = Builder.objects.get_or_create( id = eachlead.compid )
    if builder_created_flag:
        builder_model.name = eachlead.cmpname
        builder_model.start_date = datetime.datetime.now().date()
        builder_model.package = Package.objects.get(name='default')
        builder_model.is_active = True
        builder_model.service = Service.objects.get(name = 'Site Visit')
        builder_model.save()


    # project
    project_model, project_created_flag  = Project.objects.get_or_create(
        id =  eachlead.propid
    )
    if project_created_flag:
        project_model.name =  eachlead.property
        project_model.builder = builder_model
        project_model.save()


    # country
    if eachlead.country:
        country_model, country_created_flag  = Country.objects.get_or_create(
            name =  eachlead.country
        )


    # city
    if eachlead.city:
        city_model, city_created_flag  = City.objects.get_or_create(
            name =  eachlead.city
        )

    #  web_site_url
    if eachlead.websiteurl:
        web_site_url_model, web_site_url_created_flag  = WebSiteUrl.objects.get_or_create(
            name =  eachlead.websiteurl
        )

    # source
    if eachlead.source:
        source_model, source_created_flag  = Source.objects.get_or_create(
            name =  eachlead.source
        )

    # folder
    if eachlead.fldrname:
        folder_model, folder_created_flag  = Folder.objects.get_or_create(
            name =  eachlead.fldrname
        )

    # server_id
    if eachlead.serverid:
        server_id_model, server_id_created_flag  = ServerId.objects.get_or_create(
            name =  eachlead.serverid
        )

    return (builder_model,project_model,country_model,city_model,websiteurl,source,fldrname,serverid)


# def Create_get()


def Create_Muiltiple(model,str_list,builder_model):
    elelist = []
    if (str_list):
        str_list = str_list.replace(" ", "").split(",")
        str_list = [ ele for ele in str_list if not ele or ele != "Nill" ]
        if model == "PhoneNumber":
            for each in str_list:
                each = re.findall(r'\d+',each)
                if len(each) != 0:
                    each = each[0]
                    exist = PhoneNumber.objects.filter(number = str_encode(each,True)).filter(builder = builder_model)
                    if len(exist) == 0 :
                        phone_models = PhoneNumber(
                                    number = each,
                                    builder = builder_model)
                        phone_models.clean()
                        phone_models.save()
                    else:
                        phone_models = exist[0]
                        
                    elelist.append(phone_models)

        elif model == "Emailaddress":
            for each in str_list:
                exist = Emailaddress.objects.filter(mail_id = str_encode(each,False)).filter(builder = builder_model)
                if len(exist) == 0 :
                    email_models = Emailaddress(
                                mail_id = each,
                                builder = builder_model)
                    email_models.clean()
                    email_models.save()
                else:
                    email_models = exist[0]

                elelist.append(email_models)

    return elelist





# def phonecreate(visphone,builder_model):
    
    
# def mailcreate(visemail,builder_model):
    
        








        # # [ create_email(email)  for email in mail_ids] 
        # # """ remove special characters from phone like 
        # #  ['!', '"', '#', '$', '%', '&', "'", '(', ')', 
        # #  '*', '+', ',', '-', '.', '/', ':', ';', '<',
        # #  '=', '>', '?', '@', '[', '\\', ']', '^', 
        # #  '_', '`', '{', '|', '}', '~']
        # # """
        # # for each_character in punctuation:
        # #     if each_character != ",":
        # #         visphone = visphone.replace(each_character,"")
        
        # phone_numbers = visphone.split(',')
    
        
        # for eachphone in phone_numbers:
        #     if eachphone !='' and eachphone !='Nill':


        #         phone_model = PhoneNumber.objects.create(
        #                                     builder=builder_model,
        #                                     number=encrypted_phone,
        #                                     status_error = ("" if phonevalidation else "Invalid")
        #                                 )
        #         phonelist.append(phone_model)



# def create_email(email):
#     status_error = ""
#     domain = ""
#     try:
#         v = validate_email(email) # validate and get info
#         email = v["email"] # replace with normalized form
#         domain = v['domain']
#     except EmailNotValidError as e:
#         status_error = str(e)

#     encrypted_email = str_encode(email,False)

#     mail_model = Emailaddress.objects.create(
#                         builder = builder_model,
#                         mail_id = encrypted_email,
#                         domain = domain,
#                         status_error = status_error
#                     )
#     return mail_model





# def mailcreate(visemail,builder_model):
#     maillist = []
#     if (visemail):
#         # mail_ids = visemail.replace(" ","").split(',')
#         mail_ids = format_email(visemail)
#         maillist = [create_email(email) for email in mail_ids]
#         # for email in mail_ids:
#         #     # if email !='' and email !='Nill':
#         #     status_error = ""
#         #     domain = ""
#         #     try:
#         #         v = validate_email(email) # validate and get info
#         #         email = v["email"] # replace with normalized form
#         #         domain = v['domain']
#         #     except EmailNotValidError as e:
#         #         status_error = str(e)

#         #     encrypted_email = str_encode(email,False)

#         #     mail_model = Emailaddress.objects.create(
#         #                         builder = builder_model,
#         #                         mail_id = encrypted_email,
#         #                         domain = domain,
#         #                         status_error = status_error
#         #                     )

#         #     maillist.append(mail_model)

#     return maillist
