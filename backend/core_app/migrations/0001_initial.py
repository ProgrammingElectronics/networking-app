# Generated by Django 3.2.9 on 2022-01-05 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(max_length=250)),
                ('is_professional', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=10)),
                ('linkedin_url', models.CharField(max_length=250)),
                ('github_url', models.CharField(max_length=250)),
                ('img_url', models.CharField(max_length=250)),
                ('about_me', models.TextField(max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]