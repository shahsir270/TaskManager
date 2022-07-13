# Generated by Django 4.0.6 on 2022-07-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Assigned', 'Assigned'), ('In progress', 'In progress'), ('Under Review', 'Under Review'), ('Done', 'Done')], max_length=16, null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]