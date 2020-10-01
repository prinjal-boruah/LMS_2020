from django.db import models

from django.conf import settings



from management.models import Builder


class BuilderCallInfoKookoo(models.Model):

    name = models.CharField(db_column='name', max_length=100, blank=True, null=True)

    api_key = models.CharField(db_column='api_key', max_length=100, blank=True, null=True)

    text_to_play = models.CharField(db_column='text_to_play', max_length=100, blank=True, null=True)

    caller_id = models.CharField(db_column='caller_id', max_length=100, blank=True, null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    modified = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return str(self.name)



class BuilderCallInfo(models.Model):

    builder = models.OneToOneField(Builder,on_delete=models.CASCADE,primary_key=True)

    TYPE_CHOICES = (
        ('KooKoo', 'KooKoo'),

    )

    default_number = models.CharField(max_length=20,choices=TYPE_CHOICES, blank=True, null=True)

    type_of_connection = models.CharField(max_length=20,choices=TYPE_CHOICES, blank=True, null=True)

    builder_call_info_kookoo = models.ForeignKey(BuilderCallInfoKookoo, on_delete=models.CASCADE,blank=True, null=True)







class RequestLog(models.Model):

    response_sid = models.CharField(max_length=30,null=True, blank=True)

    requested_at = models.DateTimeField(db_index=True)

    response_ms = models.PositiveIntegerField(default=0)

    requested_params = models.TextField(null=True, blank=True)

    requested_status_code = models.PositiveIntegerField(null=True, blank=True)

    requested_method = models.CharField(max_length=10)

    requested_response = models.TextField(null=True, blank=True)

    requested_errors = models.TextField(null=True, blank=True)

    requested_url = models.URLField()

    # application specific

    user_remote_addr = models.GenericIPAddressField()

    user_host = models.URLField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Request Log'

    def __str__(self):
        return '{} {}'.format(self.requested_method, self.requested_url)




from management.models import CustomUser, PhoneNumber
# Kookoo
class TelePhonekookoo(models.Model):

    id = models.BigAutoField(primary_key=True)

    sid = models.CharField(unique=True,max_length=255)

    TYPE_CHOICES = (
        ('In', 'Incomming'),
        ('Out','Outgoing')

    )

    call_type = models.CharField(max_length=20,choices=TYPE_CHOICES, blank=True, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Field name made lowercase.

    lead = models.IntegerField(null=True, blank=True)

    phone = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE,null=True, blank=True)

    status = models.TextField(null=True, blank=True)

    url = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.pk)
