from django.db import models
from management.models import Builder, Project, Emailaddress
# Create your models here.



class BuilderEmailInfo(models.Model):

    builder = models.OneToOneField(Builder,on_delete=models.CASCADE,primary_key=True)

    email_status = models.BooleanField(default="True",db_column='is_email_settings')

    email_username = models.CharField(db_column='Username', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    email_password = models.CharField(db_column='Password', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    email_host = models.CharField(db_column='Host', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    email_port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    
    email_smtpsecure = models.CharField(db_column='SMTPSecure', max_length=5, blank=True, null=True)  # Field name made lowercase.
    
    email_smtpauth = models.IntegerField(db_column='SMTPAuth', blank=True, null=True)  # Field name made lowercase.
    
    email_ccaddress = models.CharField(db_column='CCAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
  
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
  
    def __str__(self):
        return self.builder.name





# from management.models import Lead

class Mail(models.Model):

    id = models.BigAutoField(primary_key=True)

    subject = models.CharField(max_length=250)

    body = models.TextField()

    mailid = models.ForeignKey(Emailaddress,on_delete=models.CASCADE,null=True)

    # leadida = models.ForeignKey(Lead, on_delete=models.CASCADE)
  
    builderid = models.ForeignKey(Builder, on_delete=models.CASCADE)  # Field name made lowercase.

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.builderid)






class filesattached(models.Model):
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.projectid.property_name



class ReportTemplates(models.Model):
    name = models.CharField(max_length=200)
    selectedO = models.TextField(blank=True, null=True)
    filteredO = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.name


class ReportTemplatesassigin(models.Model):
    builderid = models.ForeignKey(Builder, on_delete=models.CASCADE)
    reportTemplatesid = models.ForeignKey(ReportTemplates, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.builderid.buildername















# from dashboard.models import Lead, Property

EMAIL_STATUS = {
    -1: "Error",
    0: "Que",
    1: "Sent"}


def get_upload_path(instance, filename):
    return "{}/{}".format(
        "ext_attachment", filename)


class MinMaxInt(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MinMaxInt, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(MinMaxInt, self).formfield(**defaults)


class ExternalAttachment(models.Model):
    """
    Defines external attachment mapped against project
    """
    property_name = models.ManyToManyField(Project)
    file_name = models.CharField(max_length=100)
    file_object = models.FileField(upload_to=get_upload_path)
    creation_time = models.DateTimeField(auto_now_add=True, null=True)
    modified_time = models.DateTimeField(auto_now=True, null=True)

    def clean(self):
        if not self.file_name:
            self.file_name = self.file_object.name
        return self

    def __str__(self):
        return self.file_name


class Email(models.Model):
    """
    Individual Email status
        Lead ID: Connected externally (non unique-query for last record)
        tries: Maximum number of time tried to send succesfully
        (success as in internal function call)
    """
    email_codes = [
        (status, EMAIL_STATUS.get(status)) for status in EMAIL_STATUS]

    # lead_ida = models.ForeignKey(Lead, on_delete=models.CASCADE,null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    mail_id = models.ForeignKey(Emailaddress,on_delete=models.CASCADE,null=True)
    subject = models.CharField(max_length=250, null=True)
    message_content = models.TextField(null=False, default="Text")
    tries = MinMaxInt(min_value=0, max_value=5, default=0)
    status = models.IntegerField(choices=email_codes, default=0)
    ext_attachments = models.ManyToManyField(
        ExternalAttachment,blank=True,null=True)
    # ext_attachments = models.ManyToManyField(
    #     ExternalAttachment)


    def __str__(self):
        return "{}".format(self.id)


class InlineAttachment(models.Model):
    """
    Handle Inline attachment and coverts them to the djangoMIME
    objects will be deleted periodically / after sending an EMail
    """
    file_name = models.CharField(max_length=250)
    file_object = models.FileField(upload_to="attachment")
    creation_time = models.DateTimeField(auto_now_add=True, null=True)
    status = models.NullBooleanField()

    def __str__(self):
        return self.file_name


class EmailTemplate(models.Model):
    """
    Predefined message body for the templates
    """
    template_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Template name",
        help_text="This has to be unique")

    message_content = models.TextField()
    projects = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.template_name


        