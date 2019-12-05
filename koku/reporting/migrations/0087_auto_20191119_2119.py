# Generated by Django 2.2.4 on 2019-11-19 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0086_auto_20191120_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocpazurecostlineitemdailysummary',
            name='report_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.OCPUsageReportPeriod'),
        ),
        migrations.AddField(
            model_name='ocpazurecostlineitemprojectdailysummary',
            name='report_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.OCPUsageReportPeriod'),
        ),
    ]
