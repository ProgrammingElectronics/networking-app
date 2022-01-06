# Generated by Django 3.2.9 on 2022-01-06 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0007_alter_experience_years'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bootcamp',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='connections',
        ),
        migrations.AlterField(
            model_name='experience',
            name='industry',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='core_app.industry'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='profile',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='core_app.profile'),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graduation_year', models.CharField(blank=True, max_length=4)),
                ('graduation_status', models.CharField(choices=[('enrolled', 'Enrolled'), ('graduated', 'Graduated')], max_length=255)),
                ('bootcamp', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='core_app.bootcamp')),
                ('profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='core_app.profile')),
            ],
        ),
    ]