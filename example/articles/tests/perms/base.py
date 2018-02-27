from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from articles.models import Article


class ArticleTestCase(TestCase):

    def _get_content_type(self):
        return ContentType.objects.get_for_model(Article)


class ArticleUserPermTestCase(ArticleTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@example.com',
            is_active=True,
        )

    def _get_perm(self):
        return self.user.perms.all().get()


class ArticleGroupPermTestCase(ArticleTestCase):

    def setUp(self):
        self.group = Group.objects.create(
            name='test group',
        )

    def _get_perm(self):
        return self.group.perms.all().get()
