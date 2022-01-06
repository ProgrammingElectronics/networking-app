# Generated by Django 3.2.9 on 2022-01-06 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='connections',
            field=models.ManyToManyField(blank=True, related_name='_core_app_profile_connections_+', to='core_app.Profile'),
        ),
        migrations.CreateModel(
            name='Connection_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=255)),
                ('from_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='core_app.profile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='core_app.profile')),
            ],
        ),
    ]