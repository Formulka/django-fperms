from django.db import models

from django_perms.models import PermModel


class Article(PermModel):

    name = models.CharField(verbose_name='name', max_length=60)
    text = models.TextField(verbose_name='text')

    class Meta(PermModel.Meta):
        perms_per_instance = True
