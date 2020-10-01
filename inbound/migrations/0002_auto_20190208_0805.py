# Generated by Django 2.1.3 on 2019-02-08 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('inbound', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuilderAutoAssignInfo',
            fields=[
                ('builder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='management.Builder')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_bd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lastbd', to=settings.AUTH_USER_MODEL)),
                ('last_tme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lasttme', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeadAssignPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agentL', to=settings.AUTH_USER_MODEL)),
                ('projects', models.ManyToManyField(blank=True, db_column='Fiels Changed', to='management.Project')),
                ('who_updated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_updatedL', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LiveChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional', models.TextField(blank=True, db_column='Additional', null=True)),
                ('chat_url', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('folder', models.ForeignKey(blank=True, db_column='Folder', null=True, on_delete=django.db.models.deletion.CASCADE, to='inbound.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='ServerId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebSiteUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='livechat',
            name='server_id',
            field=models.ForeignKey(blank=True, db_column='ServerId', null=True, on_delete=django.db.models.deletion.CASCADE, to='inbound.ServerId'),
        ),
        migrations.AddField(
            model_name='livechat',
            name='source',
            field=models.ForeignKey(blank=True, db_column='Source', null=True, on_delete=django.db.models.deletion.CASCADE, to='inbound.Source'),
        ),
        migrations.AddField(
            model_name='livechat',
            name='web_site_url',
            field=models.ForeignKey(blank=True, db_column='WebSiteUrl', null=True, on_delete=django.db.models.deletion.CASCADE, to='inbound.WebSiteUrl'),
        ),
        migrations.AddField(
            model_name='agentavailability',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agentavailability',
            name='who_updated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]