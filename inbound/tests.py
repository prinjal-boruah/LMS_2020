
from django.test import TestCase
from django.urls import reverse
import datetime


from management.models import *
from inbound.models import *
from dashboard.models import *


class PushTestCase(TestCase):

    aa = {
            'chVisitid':'12345678901234567892',
            'compid':'50',
            'cmpname':'fdsfsdf',
            'propid':'510',
            'property':'sdfsd',
            'visemail':'sdfsd@gfdg.com',
            'visphone':'8867523005',
            'leadDate':'2018-01-24',
            'customerName':'virat12',
            'country':'india',
            'city':'bng',
            'fldrname':'dfgg',
            'serverid':'dfgdfg',
            'websiteurl':'gdfgdf.com',
            'additional':"{'dsffsd':'fdsdfsdfs'}",
            'source':'sdfdsfsdfsfsdfs'
        }
 

    @classmethod
    def setUpTestData(self):
        # from management.start import createNewInstance
        # createNewInstance()
        pass
        


    def test_to_assign_Testing(self):

        """
        Push the  lead assgin testing 
        """
        print('Push the lead test_to_push_mandatery out mandatery')
        for each in range(20):
            data = self.aa.copy()
            data['chVisitid'] =  str(int(data['chVisitid']) + 1)
            data['visemail'] =  data['visemail'] + str(each)
            data['visphone'] =  str(int(data['visphone']) + 1)
            response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
            self.assertEqual(response.status_code,201)
            
        for each in range(2):
            data = self.aa.copy()
            data['chVisitid'] =  str(int(data['chVisitid']) + 1)
            data['visphone'] = '8854572222,9876543210'
            response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
            self.assertEqual(response.status_code,201)

        # # print('disbled the auto assign part')
        # # builder2 = Builder.objects.get(id='50')
        # # builder2.is_auto_assign_tme = False  
        # # builder2.save()
        # response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
        # self.assertEqual(response.status_code,201)



        # # print('Enable the auto assign part')
        # # builder22 = Builder.objects.get(id='50')
        # # builder22.is_auto_assign_tme = True  
        # # builder22.save()
        # data['chVisitid'] =  str(int(data['chVisitid']) + 1)
        # response2 = self.client.post(path='/inbound/v5/api/livechat/',data=data)
        # self.assertEqual(response2.status_code,201)

    
    
    
    # def test_to_push_all(self):


    #     """
    #     Push the lead just like the API 
    #     """
    #     response = self.client.post(path='/inbound/v5/api/livechat/',data=self.aa)
    #     self.assertEqual(response.status_code, 201)
    #     print('Phone \n',PhoneNumber.objects.all().values())
    #     self.assertEqual(len(PhoneNumber.objects.all()),2)
    #     print('Lead \n',Lead.objects.all().values())
    #     self.assertEqual(len(Lead.objects.all())>0,True)
    #     print('LeadActivity \n',LeadActivity.objects.all().values())
    #     self.assertEqual(len(LeadActivity.objects.all())>0,True)
    #     print('FielsChanged \n', FielsChanged.objects.all().values())
    #     self.assertEqual(len(FielsChanged.objects.all())>0,True)






    # def test_to_push_mandatery1(self):
    #     """
    #     Push the lead with out mandatery
    #     """

    #     print('\n\nPush the lead with out mandatery')
    #     data = self.aa.copy()

    #     mandatery =[
    #             'chVisitid',
    #             'compid', 'cmpname', 
    #             'propid', 'property',
    #             'leadDate',
    #             'fldrname','serverid',
    #             ]

    #     for each in mandatery:
    #         data['chVisitid'] =  str(int(data['chVisitid']) + 1)
    #         data[each] = ''
    #         response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
    #         data = self.aa.copy()
    #         self.assertEqual(response.exception,True)


    
    # def test_to_push_mandatery(self):

    #     """
    #     Push the  lead with out phone and email mandatery
    #     """
    #     print('Push the lead test_to_push_mandatery out mandatery')
    #     data = self.aa.copy()

    #     mandatery =[
    #             'visemail',
    #             'visphone',
    #             ]


    #     data['chVisitid'] =  str(int(data['chVisitid']) + 1)
    #     data[mandatery[0]] = ''
    #     response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
    #     self.assertEqual(response.exception,False)

    #     data['chVisitid'] =  str(int(data['chVisitid']) + 1)
    #     data[mandatery[0]] = self.aa[mandatery[0]]
    #     data[mandatery[1]] = ''
    #     response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
    #     self.assertEqual(response.exception,False)

    #     data['chVisitid'] =  str(int(data['chVisitid']) + 1)
    #     data[mandatery[0]] = ''
    #     data[mandatery[1]] = ''
    #     response = self.client.post(path='/inbound/v5/api/livechat/',data=data)
    #     self.assertEqual(response.exception,True)




      
