from django.db import models
from management.models import Project


class PushAPI(models.Model):
    # builder = models.OneToOneField(Builder,on_delete=models.CASCADE,primary_key=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    api_name = models.CharField(max_length=30, blank=True, null=True)
    api_URL = models.CharField(max_length=100, blank=True, null=True,db_column='apiURL or CLI')
    condition_status = (
        ('NO', 'All'),
        ('CO', 'COMPLETED'),

    )
    condition = models.CharField(db_column='condition', max_length=2, choices=condition_status,default='NO')  # Field name made lowercase.
    is_post_method = models.BooleanField(default="True")
    is_active = models.BooleanField(default="False")
    api_parametejsonstring = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)


class PushMail(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    to_mail = models.CharField(max_length=100)
    is_Active = models.BooleanField(default="False")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)


from management.models import Lead

class PushFlags(models.Model):
    lead = models.OneToOneField(Lead,on_delete=models.CASCADE)
    mail_flag = models.BooleanField(default="False")
    api_flag = models.BooleanField(default="False")


class PushLog(models.Model):
    REQUEST_TYPE_CHOICES = (
        ('Mail', 'Mail'),
        ('RestAPI','RestAPI')

    )
    request_type = models.CharField(max_length=20,choices=REQUEST_TYPE_CHOICES, blank=True, null=True)
    requested_at = models.DateTimeField(db_index=True)
    response_ms = models.PositiveIntegerField(default=0)
    requested_params = models.TextField(null=True, blank=True)
    requested_status_code = models.PositiveIntegerField(null=True, blank=True)
    requested_method = models.CharField(max_length=10)
    requested_response = models.TextField(null=True, blank=True)
    requested_errors = models.TextField(null=True, blank=True)
    requested_url = models.URLField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Request Log'

    def __str__(self):
        return '{} {}'.format(self.requested_method, self.requested_url)