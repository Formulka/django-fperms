from django.db import models


class Article(models.Model):

    name = models.CharField(verbose_name='name', max_length=60)
    text = models.TextField(verbose_name='text')
