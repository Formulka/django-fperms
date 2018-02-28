from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from articles.models import Article

from .factories import UserFactory, GroupFactory


class ArticleTestCase(TestCase):

    def _get_content_type(self):
        return ContentType.objects.get_for_model(Article)


class ArticleUserPermTestCase(ArticleTestCase):

    def setUp(self):
        self.user = UserFactory()


class ArticleGroupPermTestCase(ArticleTestCase):

    def setUp(self):
        self.group = GroupFactory()
