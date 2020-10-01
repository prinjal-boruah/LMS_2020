
import json
import base64

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from management.models import *


from .forms import EmailForm
from .models import EmailTemplate, InlineAttachment


from pprint import pprint



def get_templates(lead_idx):
    """
    Retrieves the Email template, formats for XML rendering
    """
    templates = []
    if lead_idx:
        try:
            lead_idx = int(lead_idx)
        except TypeError:
            pass
        project = Lead.objects.filter(id=lead_idx).last()
        if project:
            data_templates = EmailTemplate.objects.filter(
                projects=project.project).values(
                    "template_name", "id")
            # data_templates = EmailTemplate.objects.filter().values(
            #         "template_name", "id")
            for data in data_templates:
                templates.append({
                    "template_name": data.get("template_name"),
                    "template_id": "/emailx/template/?template_id={}".format(
                        data.get("id"))})
    return templates


@method_decorator(csrf_exempt, name='dispatch')
class FileUpload(View):
    """
    Accepts any kind of file and returns a link
    Please make sure, you have given sufficient access to store files
    """

    def get(self, request):
        print(request.GET)
        return JsonResponse({"message": "get"})

    def post(self, request):
        response = {"location": "http://googlex.com"}
        data = request.FILES
        try:
            filename = data.dict().get("file").name
            form = InlineAttachment(
                file_name=filename,
                file_object=data.dict().get("file"))
            form.save()
            response = {
                "location": "http://{}/media/{}".format(
                    request.META['HTTP_HOST'], form.file_object)}
        except:
            pass
        return JsonResponse(response)


class EmailComposer(View):
    """
    Handles Email Compose form for TME
        Renders form with attachment fields filtered for the given
        lead id
            Lead->Project->
            ExternalAttachment->Project=>Attachments
    """

    def get(self, request):
        """
        Filter attachments and render the HTML form
        """
        template_name = "emailx/composer.html"
        variables = {
            "sitetitle": "Composer",
            "emailform": EmailForm(
                initial={'lead_id': request.GET.get("lead_id")}),
            "templates": get_templates(request.GET.get("lead_id"))}
        return render(request, template_name, context=variables)

    def post(self, request):
        """
        Renders the Email cmpose form and collects data
        """
        
        response = {"error": "There was an error with your submisssion"}
        # formdata = json.loads("{"+request.body.decode("utf-8")+"}" )
        data = {
            "mail_id": request.POST.get("mail_id"),
            "subject": request.POST.get("subject"),
            "message_content": request.POST.get("message_content"),
            "ext_attachments": request.POST.get("ext_attachments","")
        }
        # formdata = json.loads(request.body.decode("utf-8"))
        form = EmailForm(
            initial={'lead_id': request.GET.get("lead_id")},
            data=data)
        if form.is_valid():
            try:
                # form.cleaned_data()
                form.save()
                response = {"success": "Sending mail is scheduled"}
            except Exception as e:
                pprint("ERROR")
                pprint(e)
                # response['error2'] = e by prinjal
                pass
        else:
            pprint(form.errors)
            import pdb; pdb.set_trace()

        # need to add the lead status here 

        return JsonResponse(response)

        # pprint("Testing Post")
        
        # import pdb; pdb.set_trace()

       

        # print(data)



        
        #     pass


class TemplateLoader(View):
    """
    Frontend will request for a particular template ID,
    that will be fetched from database and rendered (HTTP) back.
    """

    def get(self, request):
        content = None
        template_id = request.GET.get("template_id", None)
        if template_id:
            try:
                templates = EmailTemplate.objects.get(id=template_id)
                if templates:
                    content = templates.message_content
            except ObjectDoesNotExist:
                pass
        return HttpResponse(content)