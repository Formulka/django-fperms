from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client

from articles.models import Article

from .factories import UserFactory, GroupFactory


class ArticleTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = Client()

    def _get_content_type(self):
        return ContentType.objects.get_for_model(Article)


class ArticleUserPermTestCase(ArticleTestCase):
    pass


class ArticleGroupPermTestCase(ArticleTestCase):

    def setUp(self):
        super().setUp()
        self.group = GroupFactory()
