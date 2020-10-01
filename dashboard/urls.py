"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from dashboard import views 
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(), name='logout'),
    path('lead/<slug:slug>/',views.Leads.as_view()),
    path('lead/',csrf_exempt(views.Leads.as_view())),
    path('leadEdit/',csrf_exempt(views.LeadEdit.as_view())),
    path('leadDataLoad/<slug:slug>/',csrf_exempt(views.LeadDataLoad.as_view())),
    path('settings/',csrf_exempt(views.Settings.as_view()),name='settings'),

    path('management/<slug:slug>/',csrf_exempt(views.Managements.as_view())),
]
