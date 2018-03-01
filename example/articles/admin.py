from django.contrib import admin
from django_perms.admin import PermAdmin

from articles.models import Article


@admin.register(Article)
class ArticleAdmin(PermAdmin):

    perms_per_instance = True
