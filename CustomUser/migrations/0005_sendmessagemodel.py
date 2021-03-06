# Generated by Django 2.2.7 on 2019-11-30 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0004_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=150)),
                ('fromperson', models.CharField(max_length=150)),
                ('frompost', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('edit_count', models.IntegerField(default=0)),
                ('mainmessage', models.TextField(max_length=500)),
            ],
        ),
    ]
