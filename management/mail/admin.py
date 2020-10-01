from email.mime.image import MIMEImage

from bs4 import BeautifulSoup as BS
from django.contrib import admin
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.http import HttpResponse
from django_rq import job

from .forms import AttachmentForm, EmailForm, EmailTemplateForm, ExternalAttachmentForm
from .models import BuilderEmailInfo, Email, InlineAttachment, ExternalAttachment, EmailTemplate


@job
def send_test_mail(queryset):
    if queryset.count() > 1:
        return "Cannot send Email to more than 1"
    else:
        email_status = -1
        data = queryset[0]
        msg = EmailMultiAlternatives(
            "Subject here",
            "text_content",
            "kabhishek@livserv.com",
            ["kabhishek@livserv.com"],
            ["livserv.gcloud1@gmail.com"],
            headers={'Message-ID': 'foo'})
        htmlcontent = data.message_content
        htmlsoup = BS(htmlcontent, "lxml")
        images = htmlsoup.find_all("img", src=True)
        images = [img.attrs.get("src") for img in images]
        print("images", images)
        if images:
            for img in images:
                filename = img.replace("/media/attachment/", "")
                print(filename)
                try:
                    image = InlineAttachment.objects.get(file_name=filename)
                    imagex = MIMEImage(image.file_object.read())
                    imagex.add_header(
                        'Content-ID', '<{}>'.format(image.file_name))
                    htmlcontent = htmlcontent.replace(
                        img, "cid:{}".format(filename))
                    msg.attach(imagex)
                except Exception as e:
                    print("exception:", e)
        msg.mixed_subtype = 'related'
        msg.content_subtype = "html"  # Main content is now text/html
        msg.attach_alternative(htmlcontent, "text/html")
        try:
            msg.send()
            email_status = 1
        except Exception as e:
            print(e)
        data.status = email_status
        data.save()
        return email_status
send_test_mail.short_description = "Send Test mail"

class EmailAdmin(admin.ModelAdmin):

    form = EmailForm
    list_display = [
        # "lead_id",
        "status",]
        # "boolean_status"]

    actions = ["send_test_mailx",]

    def send_test_mailx(self, request, queryset):
        data = send_test_mail.delay(queryset)

    send_test_mailx.short_description = "Send Test mail"


class AttachementAdmin(admin.ModelAdmin):
    form = AttachmentForm


class ExternalAttachmentAdmin(admin.ModelAdmin):
    form = ExternalAttachmentForm
    exclude = ["file_name",]

class TemplateAdmin(admin.ModelAdmin):
    form = EmailTemplateForm

class BuilderEmailInfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(BuilderEmailInfo, BuilderEmailInfoAdmin)

admin.site.register(Email, EmailAdmin)
admin.site.register(InlineAttachment, AttachementAdmin)
admin.site.register(ExternalAttachment, ExternalAttachmentAdmin)
admin.site.register(EmailTemplate, TemplateAdmin)
