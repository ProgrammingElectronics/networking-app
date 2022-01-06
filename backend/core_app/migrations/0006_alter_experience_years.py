# Generated by Django 3.2.9 on 2022-01-06 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0005_alter_connectionrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='years',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=255),
        ),
    ]