from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_perms.models import Perm, GlobalPerm, ObjectPerm, FieldPerm

from .models import Article


class ArticlePermissionTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@example.com',
            is_active=True,
        )

    def test_add_perm(self):
        perm = Perm.objects.create(
            name='article permission',
            codename='add',
            content_type=ContentType.objects.get_for_model(Article),
        )

        self.user.add_perm(perm, model=Article)

    def test_add_global_perm(self):

        global_perm = GlobalPerm.objects.create(
            name='global permission',
            codename='export',
        )

        self.user.add_perm(global_perm)

    def test_add_object_perm(self):
        article = Article.objects.create(
            name='the name',
            text='lorem ipsum'
        )

        object_perm = ObjectPerm.objects.create(
            name='article object permission',
            codename='object',
            content_object=article,
        )

        self.user.add_perm(object_perm, obj=article)

    def test_add_field_perm(self):
        field_perm = FieldPerm.objects.create(
            name='article object permission',
            codename='field',
            content_type=ContentType.objects.get_for_model(Article),
            field_name='name',
        )

        self.user.add_perm(field_perm, model=Article)
