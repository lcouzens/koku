# Generated by Django 2.1 on 2018-09-21 19:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import tenant_schemas.postgresql_backend.base
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('account_id', models.CharField(max_length=150, null=True)),
                ('org_id', models.CharField(max_length=150, null=True)),
                ('schema_name', models.TextField(default='public', unique=True)),
            ],
            options={
                'ordering': ['schema_name'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('AWS', 'AWS'), ('OCP', 'OCP')], default='AWS', max_length=50)),
                ('setup_complete', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProviderAuthentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('provider_resource_name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProviderBillingSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bucket', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('preference', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('name', models.CharField(default=uuid.uuid4, max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='provider',
            name='authentication',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ProviderAuthentication'),
        ),
        migrations.AddField(
            model_name='provider',
            name='billing_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ProviderBillingSource'),
        ),
        migrations.AddField(
            model_name='provider',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.User'),
        ),
        migrations.AddField(
            model_name='provider',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Customer'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('account_id', 'org_id')},
        ),
        migrations.AlterUniqueTogether(
            name='userpreference',
            unique_together={('name', 'user')},
        ),
    ]
