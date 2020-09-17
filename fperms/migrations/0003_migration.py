# Generated by Django 3.1.1 on 2020-09-16 12:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fperms', '0002_auto_20180713_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perm',
            name='type',
            field=models.CharField(choices=[('generic', 'generic'), ('model', 'model'), ('object', 'object')],
                                   default='generic', max_length=10),
        ),
        migrations.AlterField(
            model_name='perm',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='fperms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(blank=True, max_length=100, null=True, unique=True,
                                              verbose_name='codename')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('fgroups', models.ManyToManyField(blank=True, related_name='parents', to='fperms.Group')),
                ('fperms', models.ManyToManyField(blank=True, related_name='fgroups', to='fperms.Perm')),
                ('users', models.ManyToManyField(blank=True, related_name='fgroups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'ordering': ('codename',),
            },
        ),
    ]