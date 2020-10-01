from django.urls import path
from .views import EmailComposer, FileUpload, TemplateLoader

urlpatterns = [

    path('', FileUpload.as_view(), name="fileupload"),
    path('composer/',EmailComposer.as_view(), name="composer"),
    path('template/',TemplateLoader.as_view(), name="template"),
  
]
