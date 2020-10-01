from django.contrib import admin
from django.urls import path, include 
from django.views.decorators.csrf import csrf_exempt
from notifcation.views import  *

urlpatterns = [
    path('call/',csrf_exempt(CallNotifcationView.as_view())),
    path('alert/',csrf_exempt(AlertNotifcationView.as_view())),
    path('notification/',csrf_exempt(NotifcationView.as_view())),
    path('info/',csrf_exempt(InfoNotifcationView.as_view())),
    path('incomingalert/',csrf_exempt(IncomingalertView.as_view())),

]
