import base64
import pdb
import re

from django.conf import settings


def str_encode(encodinging_string,phone_or_email_flag):
    # finding first digit from scerate key
    m = re.search("\d", settings.SECRET_KEY)

    # adding one because at least it convert  
    number_of_encode = (int(settings.SECRET_KEY[m.start()]) % 3) + 1

    mixingstring = settings.SECRET_KEY[:len(encodinging_string)]
    
    
    if phone_or_email_flag:
        mixingnumber = ''
        for each in mixingstring:
            mixingnumber += str(ord(each))
        mixingnumber = mixingnumber[:len(encodinging_string)]

        pre_enconding_string = ''
        
        for count,each in enumerate(encodinging_string):
            pre_enconding_string += each + mixingnumber[count]

        enconding_string = pre_enconding_string.encode() 
        # number of time encodeing with base64
        for en_count in range(number_of_encode):
            enconding_string = base64.b64encode(enconding_string)
        
        return enconding_string.decode()
    
    else:
        pre_enconding_string = ''
        if len(mixingstring) > len(encodinging_string):
            mixingnumber = mixingstring[:len(encodinging_string)]
        else:
            mixingnumber = mixingstring[:len(encodinging_string)]
            mixingnumber = mixingnumber * 10

        for count,each in enumerate(encodinging_string):
            pre_enconding_string += each + mixingnumber[count]

        enconding_string = pre_enconding_string.encode() 
        # number of time encodeing with base64
        for en_count in range(number_of_encode):
            enconding_string = base64.b64encode(enconding_string)
        
        return enconding_string.decode()






def str_decode(dencodinging_string):
    # import pdb;pdb.set_trace()

    m = re.search("\d", settings.SECRET_KEY)

    # adding one because at least it convert  
    number_of_encode = (int(settings.SECRET_KEY[m.start()]) % 3) + 1

    dencodinging_string = dencodinging_string.encode()
    # number of time dencodeing with base64
    for en_count in range(number_of_encode):
        dencodinging_string = base64.b64decode(dencodinging_string)

    post_enconding_string = ''
    dencodinging_string = dencodinging_string.decode()
        
    for count,each in enumerate(dencodinging_string):
        if count % 2 == 0:
            post_enconding_string += each

    return post_enconding_string



"""

phone = validated_data['phone']['number'].split(',')[0]

(Pdb) en = str_encode(phone,True)
(Pdb) str_decode(en)
*** TypeError: must be str, not int
(Pdb) str_decode('fdsfs')


post

"""