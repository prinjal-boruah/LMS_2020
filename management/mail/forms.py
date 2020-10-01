"""
Full featured web editing
==========================

Renders and updates the EMAIL composer (django model form)

    Uses TinyMCE package for HTML Field with ability to prefill the
rich text to the composer.

TinyMCE : https://www.tinymce.com
"""
import base64
from django.forms import (CheckboxSelectMultiple, HiddenInput,
                          ModelForm, ModelMultipleChoiceField)

# from management import *


from .models import Email, EmailTemplate, ExternalAttachment, InlineAttachment
from management.models import *
class EmailForm(ModelForm):
    """
    Email Form
    ===========

    Email model form, extended to prefill initial values based on
    visitor lead id (optional).

    **LEAD ID**

    1.  *External attachments*
        Lead id is used to show appropriate External attachments along
        with the composer layout. Incase lead ID is not provided, no external
        attachments will appear.

    2.  *Templates*
        Email templates are mapped against the project, lead id is used to
        get the project id, and prefill (or in templates section) the
        available templates for the given project.
    """
    ext_attachments = ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset=ExternalAttachment.objects.all().exclude())

    def __init__(self, *args, **kwargs):
        lead_idx = None
        print(kwargs)
        initial = kwargs.get("initial")
        if initial:
            lead_idx = initial.get("lead_id")
        if lead_idx:
            super(EmailForm, self).__init__(*args, **kwargs)
            try:
                lead_idx = int(lead_idx)
            except TypeError:
                pass
            lead = Lead.objects.filter(id=lead_idx).last()
            self.fields["mail_id"].queryset = \
                Emailaddress.objects.filter(id__in=lead.email.all())
            self.fields["ext_attachments"].queryset = \
                ExternalAttachment.objects.filter(
                    property_name=lead.project)
            self.fields['ext_attachments'].required = False 
            # self.fields["lead_id"].widget = HiddenInput()
           

        else:
            super().__init__(*args, **kwargs)


    # def clean_message_content(self):
    #     data = self.cleaned_data["message_content"]
    #     return base64.b64decode(data)


    class Meta:
        model = Email
        fields = "__all__"
        exclude = ["tries", "status"]

class EmailTemplateForm(ModelForm):
    """
    Email Template Form
    ====================

    Email Template model form, is similar to Email Form, instead of
    sending the Emails, It will stored to render as an inline template
    in composer layout.
    """

    class Meta:
        model = EmailTemplate
        fields = "__all__"
        exclude = ["status", ]

    class Media:
        js = (
            "tinymce/js/tinymce/tinymce.min.js",
            "tinymce/js/tinymce/tiny_loader.js",)

class AttachmentForm(ModelForm):
    """
    Attachment Form
    ====================
        Wrapper to handle Inline attachments, without user's
    notice, Frontend script handles the event of adding a new image
    using. Uploaded image will be sent as POST request.

        This form stores the uploaded image and returns the path to access
    the image in Email composer layout and while sending Emails, these
    inline images are converted as MIME to deliver self-contained Emails.
    """

    class Meta:
        model = InlineAttachment
        fields = "__all__"
        exclude = ["status", ]


class ExternalAttachmentForm(ModelForm):
    class Meta:
        model = ExternalAttachment
        fields = "__all__"

    # def save(self, *args, **kwargs):
    #     print(self.cleaned_data)
    #     new_ext = ExternalAttachment(file_object=self.cleaned_data.get("file_object"))
    #     new_ext.save()
    #     print(new_ext)
