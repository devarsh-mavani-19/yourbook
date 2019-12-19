# Generated by Django 2.2.7 on 2019-12-02 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0006_sendmessagemodel_pdffile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmessagemodel',
            name='pdffile',
        ),
        migrations.AddField(
            model_name='bookmodel',
            name='pdffile',
            field=models.FileField(default=None, upload_to='documents/'),
        ),
    ]