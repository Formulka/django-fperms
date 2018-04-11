from django.conf import settings
from fperms.conf import settings as fperms_settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(fperms_settings.PERM_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_perms', to=fperms_settings.PERM_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_perms', to='auth.Group')),
            ],
            options={
                'verbose_name': 'group perm',
                'ordering': ('group',),
                'verbose_name_plural': 'group perms',
            },
        ),
        migrations.CreateModel(
            name='Perm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('generic', 'generic'), ('model', 'model'), ('object', 'object'), ('field', 'field')], default='generic', max_length=10)),
                ('codename', models.CharField(max_length=100, verbose_name='codename')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('object_id', models.SmallIntegerField(blank=True, null=True, verbose_name='object pk')),
                ('field_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='field name')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'permission',
                'ordering': ('codename',),
                'verbose_name_plural': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='UserPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_perms', to=fperms_settings.PERM_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_perms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user perm',
                'ordering': ('user',),
                'verbose_name_plural': 'user perms',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userperm',
            unique_together=set([('user', 'perm')]),
        ),
        migrations.AlterUniqueTogether(
            name='perm',
            unique_together=set([('type', 'codename', 'content_type', 'object_id', 'field_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupperm',
            unique_together=set([('group', 'perm')]),
        ),
    ]
