# Generated by Django 4.1.7 on 2023-05-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_form_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
