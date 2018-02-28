from django.contrib.contenttypes.models import ContentType
from django_perms.models import Perm

from articles.models import Article

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase


class FieldPermTestCaseMixin:

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


class FieldPermTestCase(FieldPermTestCaseMixin, ArticleTestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_field_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.field_perms().get())


class ArticleUserFieldPermPermTestCase(FieldPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_field_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created field perm
        self.assertEquals(perm, self.user.perms.all().get())

    def test_add_field_perm_by_str(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add('field.articles.Article.name.add')

        # test the new user perm is the created add name field perm
        self.assertEquals(add_name_perm, self.user.perms.all().get())

    def test_fail_add_field_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('field.articles.Article.name.delete')

    def test_fail_add_field_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.user.perms.add('field.articles.Foo.name.add')

    def test_fail_add_field_perm_non_existent_field_name(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('field.articles.Article.foo.add')

    def test_has_field_perm(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add(add_name_perm)

        self.assertTrue(self.user.perms.has_perm('field.articles.Article.name.add'))

    def test_fail_has_perm_non_existent_field_name(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add(add_name_perm)

        self.assertFalse(self.user.perms.has_perm('field.articles.Article.foobar.add'))

    def test_fail_has_perm_non_existent_codename(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add(add_name_perm)

        self.assertFalse(self.user.perms.has_perm('field.articles.Article.name.delete'))


class ArticleGroupFieldPermPermTestCase(FieldPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_field_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new user perm is the created field perm
        self.assertEquals(perm, self.group.perms.all().get())

    def test_add_field_perm_by_str(self):
        add_name_perm = self._create_add_perm()

        self.group.perms.add('field.articles.Article.name.add')

        # test the new user perm is the created add name field perm
        self.assertEquals(add_name_perm, self.group.perms.all().get())

    def test_fail_add_field_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('field.articles.Article.name.delete')

    def test_fail_add_field_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.group.perms.add('field.articles.Foo.name.add')

    def test_fail_add_field_perm_non_existent_field_name(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('field.articles.Article.foo.add')
