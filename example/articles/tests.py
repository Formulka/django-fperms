from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_perms.models import Perm

from .models import Article


class ArticleUserTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@example.com',
            is_active=True,
        )

    def _get_user_perm(self):
        return self.user.perms.all().get()

    def _get_content_type(self):
        return ContentType.objects.get_for_model(Article)


class ArticleUserGlobalPermTestCase(ArticleUserTestCase):

    def _create_perm(self):
        return Perm.objects.create(
            codename='export',
        )

    def test_perm_has_a_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_global_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.global_perms().get())

    def test_add_global_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created global perm
        self.assertEquals(perm, self._get_user_perm())

    def test_add_global_perm_by_codename(self):
        export_perm = self._create_perm()

        self.user.perms.add('export')

        # test the new user perm is the created export global perm
        self.assertEquals(export_perm, self._get_user_perm())

    def test_fail_add_global_perm_by_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('export')


class ArticleUserModelPermTestCase(ArticleUserTestCase):

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            codename='add',
            content_type=self._get_content_type()
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            codename='delete',
            content_type=self._get_content_type()
        )

    def test_perm_has_a_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_model_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.model_perms().get())

    def test_add_model_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created model perm
        self.assertEquals(perm, self._get_user_perm())

    def test_add_model_perm_by_codename_and_ctype(self):
        add_perm = self._create_add_perm()

        self.user.perms.add('add', model=Article)

        # test the new user perm is the created add model perm
        self.assertEquals(add_perm, self._get_user_perm())

    def test_fail_add_model_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('delete', model=Article)

    def test_fail_add_model_perm_by_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('add', model=ContentType)


class ArticleUserObjectPermTestCase(ArticleUserTestCase):

    def setUp(self):
        super().setUp()
        self.article = Article.objects.create(name='foo', text='foo foo')
        self.article2 = Article.objects.create(name='bar', text='bar bar')

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            codename='add',
            content_object=self.article,
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            codename='delete',
            content_object=self.article,
        )

    def test_perm_has_a_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_object_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.object_perms().get())

    def test_add_object_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created object perm
        self.assertEquals(perm, self._get_user_perm())

    def test_add_object_perm_by_codename_and_object(self):
        add_obj_perm = self._create_add_perm()

        self.user.perms.add('add', obj=self.article)

        # test the new user perm is the created add object perm
        self.assertEquals(add_obj_perm, self._get_user_perm())

    def test_fail_add_object_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('delete', model=Article)

    def test_fail_add_object_perm_by_non_existent_object(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('add', obj=self.article2)


class ArticleUserFieldPermTestCase(ArticleUserTestCase):

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            codename='add',
            content_type=self._get_content_type(),
            field_name='name',
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            codename='delete',
            content_type=self._get_content_type(),
            field_name='name',
        )

    def test_perm_has_a_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_field_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.field_perms().get())

    def test_add_field_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created field perm
        self.assertEquals(perm, self._get_user_perm())

    def test_add_field_perm_by_codename_model_and_field_name(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add('add', model=Article, field_name='name')

        # test the new user perm is the created add name field perm
        self.assertEquals(add_name_perm, self._get_user_perm())

    def test_fail_add_field_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('delete', model=Article, field_name='name')

    def test_fail_add_field_perm_by_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('delete', model=ContentType, field_name='name')

    def test_fail_add_field_perm_by_non_existent_field_name(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('add', model=Article, field_name='fail')
