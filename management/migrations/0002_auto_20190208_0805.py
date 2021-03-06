# Generated by Django 2.1.3 on 2019-02-08 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('inbound', '0002_auto_20190208_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='live_chat',
            field=models.ManyToManyField(blank=True, db_column='Live Chat', to='inbound.LiveChat'),
        ),
        migrations.AddField(
            model_name='lead',
            name='phone',
            field=models.ManyToManyField(blank=True, db_column='Phone Number', to='management.PhoneNumber'),
        ),
        migrations.AddField(
            model_name='lead',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Project'),
        ),
        migrations.AddField(
            model_name='lead',
            name='repeted_leads_info',
            field=models.ManyToManyField(blank=True, db_column='APILead', to='inbound.APILead'),
        ),
        migrations.AddField(
            model_name='lead',
            name='skype',
            field=models.ManyToManyField(blank=True, db_column='Skype', to='management.Skype'),
        ),
        migrations.AddField(
            model_name='lead',
            name='tme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tme', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lead',
            name='tmebd',
            field=models.ForeignKey(blank=True, db_column='tmebd', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lead',
            name='unit_type',
            field=models.ForeignKey(blank=True, db_column='Unit Type', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.UnitType'),
        ),
        migrations.AddField(
            model_name='emailaddress',
            name='builder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder'),
        ),
        migrations.AddField(
            model_name='callstatusleadstatus',
            name='call_status',
            field=models.ForeignKey(blank=True, db_column='Call Status', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.CallStatus'),
        ),
        migrations.AddField(
            model_name='callstatusleadstatus',
            name='lead_type',
            field=models.ManyToManyField(blank=True, db_column='Lead Type', to='management.LeadStatus'),
        ),
        migrations.AddField(
            model_name='callstatusleadstatus',
            name='service',
            field=models.ForeignKey(blank=True, db_column='service', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Service'),
        ),
        migrations.AddField(
            model_name='builder',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Package'),
        ),
        migrations.AddField(
            model_name='builder',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Service'),
        ),
        migrations.AddField(
            model_name='apirequestlog',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.Lead'),
        ),
        migrations.AddField(
            model_name='apirequestlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customuser',
            name='builder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_roles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.UserRole'),
        ),
    ]
