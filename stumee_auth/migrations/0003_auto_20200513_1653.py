# Generated by Django 3.0.6 on 2020-05-13 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stumee_auth', '0002_auto_20200513_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_image',
        ),
        migrations.AddField(
            model_name='customuser',
            name='original_image',
            field=models.ImageField(blank=True, default='default_icon/default_icon1.png', upload_to='user_icon/', verbose_name='オリジナルアイコン'),
        ),
    ]
