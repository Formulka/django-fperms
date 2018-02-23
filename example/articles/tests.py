from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_perms.models import Perm

from .models import Article


class ArticleUserPermTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@example.com',
            is_active=True,
        )

    def test_add_model_perm(self):
        perm = Perm.objects.create(
            codename='add',
            content_type=ContentType.objects.get_for_model(Article),
        )

        self.user.add_perm(perm, model=Article)

        perm = self.user.get_all_perms().get()
        self.assertTrue(perm.is_model_perm)

    def test_add_global_perm(self):

        global_perm = Perm.objects.create(
            name='Global export',
            codename='export',
        )

        self.user.add_perm(global_perm)

        perm = self.user.get_all_perms().get()
        self.assertTrue(perm.is_global_perm)

    def test_add_object_perm(self):
        article = Article.objects.create(
            name='the name',
            text='lorem ipsum'
        )

        object_perm = Perm.objects.create(
            codename='object',
            content_object=article,
        )

        self.user.add_perm(object_perm, obj=article)

        perm = self.user.get_all_perms().get()
        self.assertTrue(perm.is_object_perm)

    def test_add_field_perm(self):
        field_perm = Perm.objects.create(
            codename='field',
            content_type=ContentType.objects.get_for_model(Article),
            field_name='name',
        )

        self.user.add_perm(field_perm, model=Article)

        perm = self.user.get_all_perms().get()
        self.assertTrue(perm.is_field_perm)
