# Generated by Django 4.2.10 on 2024-02-17 16:10

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
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('MEETING', 'Meeting'), ('WORKSHOP', 'Workshop'), ('CONFERENCE', 'Conference'), ('SEMINAR', 'Seminar'), ('RECRUITMENT', 'Recruitment'), ('OTHER', 'Other')], default='OTHER', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attendees', models.ManyToManyField(blank=True, related_name='attendees', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='events', to='events.tags')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ['-date'],
            },
        ),
    ]