from django.shortcuts import render
from inbound.models import *
from inbound.serializers import *

from rest_framework import viewsets

from management.mixin import LoggingMixin

from .models import *

# Create your views here.
# class Livechat()


class LiveChatLeadViewSet(LoggingMixin,viewsets.ModelViewSet):
    queryset = APILead.objects.all()
    serializer_class = livechatleadSerializer
    logging_methods = ['POST']

    


from django.views import View





class First(View):
    def get(self,request):
        from management.start import createNewInstance
        createNewInstance()
        from django.http import HttpResponse
        return HttpResponse('created')



