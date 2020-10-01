# Generated by Django 2.1.3 on 2019-02-08 08:05

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, db_column='Phone Number', max_length=100, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=100, null=True)),
                ('is_login', models.BooleanField(db_column='Is Login', default='True')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='APIRequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(db_index=True)),
                ('response_ms', models.PositiveIntegerField(default=0)),
                ('path', models.CharField(db_index=True, max_length=200)),
                ('view', models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='From Whom')),
                ('view_method', models.CharField(blank=True, db_index=True, max_length=27, null=True)),
                ('remote_addr', models.GenericIPAddressField()),
                ('host', models.URLField()),
                ('method', models.CharField(max_length=10)),
                ('query_params', models.TextField(blank=True, null=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('errors', models.TextField(blank=True, null=True)),
                ('status_code', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'API Request Log',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.CharField(db_column='Builder Id', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Builder Name', max_length=100)),
                ('limit_reached', models.IntegerField(db_column='Limit Reached', default=0)),
                ('start_date', models.DateField(blank=True, db_column='Start Date', null=True)),
                ('is_livprop_tranfer', models.BooleanField(db_column='Is Fulfilment Services', default=True)),
                ('is_encryption', models.BooleanField(db_column='Is Encryption', default=True)),
                ('is_excel_load', models.BooleanField(db_column='Is Excel Upload', default=True)),
                ('is_live_push_api', models.BooleanField(db_column='Is LiveChat Push API', default=True)),
                ('is_live_pull_api', models.BooleanField(db_column='Is LiveChat Pull API', default=True)),
                ('is_auto_assign_tme', models.BooleanField(db_column='Is Auto Assign For TME', default=True)),
                ('is_auto_assign_bd', models.BooleanField(db_column='Is Auto Assign For BD', default=True)),
                ('is_active', models.BooleanField(db_column='Is Active', default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BuyingReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CallStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('status_type', models.CharField(choices=[('Initial', 'Initial'), ('Intermediate', 'Intermediate'), ('Finish', 'Finish'), ('Negative', 'Negative')], default='Initial', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CallstatusLeadstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emailaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_id', models.CharField(db_column='email', max_length=500)),
                ('status_error', models.TextField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_id', models.CharField(db_column='vsid', max_length=20, unique=True)),
                ('source_date', models.DateField(blank=True, db_column='Source Date', null=True)),
                ('name', models.CharField(blank=True, db_column='Customer Name', max_length=150, null=True)),
                ('age', models.IntegerField(blank=True, db_column='Age', null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(18)])),
                ('designation', models.CharField(blank=True, db_column='Designation', max_length=65, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('from_unit_size', models.IntegerField(blank=True, db_column='from Unit Size', null=True)),
                ('to_unit_size', models.IntegerField(blank=True, db_column='To Unit Size', null=True)),
                ('from_budget', models.IntegerField(blank=True, db_column='From Budget', null=True)),
                ('to_budget', models.IntegerField(blank=True, db_column='To Budget', null=True)),
                ('additional_info', models.TextField(blank=True, db_column='Additional Info', null=True)),
                ('visit_date', models.DateField(blank=True, db_column='Visit Date', default='1999-01-01')),
                ('address_lat_long', models.CharField(blank=True, db_column='Address Lat Long', max_length=30, null=True)),
                ('is_livprop_tranfer', models.BooleanField(db_column='Is Fulfilment Services', default=True)),
                ('status_error', models.TextField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('bd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bd', to=settings.AUTH_USER_MODEL)),
                ('builder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder')),
                ('buying_reason', models.ForeignKey(blank=True, db_column='Buying Reason', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.BuyingReason')),
                ('city', models.ForeignKey(blank=True, db_column='City', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.City')),
                ('country', models.ForeignKey(blank=True, db_column='Country', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Country')),
                ('email', models.ManyToManyField(blank=True, db_column='Email', to='management.Emailaddress')),
                ('last_lead_activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Last_Lead_Activity', to='dashboard.LeadActivity')),
                ('lead_activity', models.ManyToManyField(blank=True, db_column='Lead Activity', to='dashboard.LeadActivity')),
            ],
        ),
        migrations.CreateModel(
            name='Leadsource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeadStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('status_type', models.CharField(choices=[('Initial', 'Initial'), ('Intermediate', 'Intermediate'), ('Finish', 'Finish'), ('Negative', 'Negative')], default='Initial', max_length=20)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeadType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Package Name', max_length=100)),
                ('validity_days', models.IntegerField(db_column='Validity', default=365, validators=[django.core.validators.MaxValueValidator(3000)])),
                ('lead_limit', models.BigIntegerField(db_column='Lead Limit', default=9223372036854775807)),
                ('tme_limit', models.IntegerField(db_column='TME Limit', default=0)),
                ('bd_limit', models.IntegerField(db_column='BD Limit', default=0)),
                ('tmebd_limit', models.IntegerField(db_column='TME/BD Limit', default=0)),
                ('is_livprop_tranfer', models.BooleanField(db_column='Is Fulfilment Services', default=True)),
                ('is_encryption', models.BooleanField(db_column='Is Encryption', default=True)),
                ('is_excel_load', models.BooleanField(db_column='Is Excel Upload', default=True)),
                ('is_live_push_api', models.BooleanField(db_column='Is LiveChat Push API', default=True)),
                ('is_live_pull_api', models.BooleanField(db_column='Is LiveChat Pull API', default=True)),
                ('is_auto_assign_tme', models.BooleanField(db_column='Is Auto Assign For TME', default='False')),
                ('is_auto_assign_bd', models.BooleanField(db_column='Is Auto Assign For BD', default='False')),
                ('is_active', models.BooleanField(db_column='Is Active', default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(db_column='Phone Number', max_length=150)),
                ('status_error', models.TextField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('builder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(db_column='Project Id', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Project Name', max_length=300)),
                ('description', models.TextField(blank=True, db_column='Project Description', null=True)),
                ('address', models.TextField(blank=True, db_column='Project Address', null=True)),
                ('is_active', models.BooleanField(db_column='Is Active', default=True)),
                ('addresslatlong', models.CharField(blank=True, db_column='Address lat long', max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('builder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder')),
                ('site_manager', models.ManyToManyField(blank=True, db_column='Site Manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Service Name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.ManyToManyField(blank=True, db_column='Lead Status', to='management.LeadStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Skype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skype_id', models.CharField(db_column='Skype Id', max_length=100)),
                ('status_error', models.TextField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('builder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Builder')),
            ],
        ),
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Role Name', max_length=50)),
                ('ui_type', models.CharField(choices=[('MA', 'Management'), ('ED', 'Editing')], default='MA', max_length=2)),
                ('user_type', models.CharField(choices=[('FA', 'Fullfilment Admin'), ('SA', 'Super Admin'), ('FT', 'Fullfilment TME'), ('FB', 'Fullfilment BD'), ('FTB', 'Fullfilment TMEBD'), ('CA', 'Client Admin'), ('CT', 'Client TME'), ('CB', 'Client BD'), ('CTB', 'Client TMEBD'), ('CUS', 'Custome')], default='CA', max_length=3)),
                ('is_encrypted', models.BooleanField(db_column='Is Encrypted', default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='lead_source',
            field=models.ForeignKey(blank=True, db_column='Lead Source', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.Leadsource'),
        ),
        migrations.AddField(
            model_name='lead',
            name='lead_type',
            field=models.ForeignKey(blank=True, db_column='Lead Type', null=True, on_delete=django.db.models.deletion.CASCADE, to='management.LeadType'),
        ),
    ]
