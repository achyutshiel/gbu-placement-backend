# Generated by Django 5.2 on 2025-04-11 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('no_of_jobs', models.IntegerField()),
                ('min_cgpa', models.FloatField()),
                ('required_skills', models.TextField()),
                ('job_role', models.CharField(max_length=255)),
                ('assessment_date', models.DateField(blank=True, null=True)),
                ('assessment_result_date', models.DateField(blank=True, null=True)),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('interview_result_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyJobSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_selected', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placement.company')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placement.studentprofile')),
            ],
        ),
    ]
