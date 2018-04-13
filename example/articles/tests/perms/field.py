from fperms import enums
from fperms.models import Perm

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase


class FieldPermTestCaseMixin:

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_FIELD,
            codename=enums.PERM_CODENAME_ADD,
            content_type=self._get_content_type(),
            field_name='name',
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_FIELD,
            codename=enums.PERM_CODENAME_DELETE,
            content_type=self._get_content_type(),
            field_name='name',
        )

    def _create_wildcard_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_FIELD,
            codename=enums.PERM_CODENAME_WILDCARD,
            content_type=self._get_content_type(),
            field_name='name',
        )


class FieldPermTestCase(FieldPermTestCaseMixin, ArticleTestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_field_perm())


class ArticleUserFieldPermPermTestCase(FieldPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_field_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add_perm(perm)

        self.user.perms.has_perm(perm)

    def test_add_field_perm_by_str(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add_perm('field.articles.Article.name.add')

        self.user.perms.has_perm(add_name_perm)

    def test_fail_add_field_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add_perm('field.articles.Article.name.delete')

    def test_fail_add_field_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.user.perms.add_perm('field.articles.Foo.name.add')

    def test_fail_add_field_perm_non_existent_field_name(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add_perm('field.articles.Article.foo.add')

    def test_has_field_perm_from_wildcard(self):
        self._create_wildcard_perm()

        self.user.perms.add_perm('field.articles.Article.name.*')

        self.assertTrue(self.user.perms.has_perm('field.articles.Article.name.whatever'))

    def test_fail_has_perm_non_existent_field_name(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add_perm(add_name_perm)

        self.assertFalse(self.user.perms.has_perm('field.articles.Article.foobar.add'))

    def test_fail_has_perm_non_existent_codename(self):
        add_name_perm = self._create_add_perm()

        self.user.perms.add_perm(add_name_perm)

        self.assertFalse(self.user.perms.has_perm('field.articles.Article.name.delete'))


class ArticleGroupFieldPermPermTestCase(FieldPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_field_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add_perm(perm)

        self.group.perms.has_perm(perm)

    def test_add_field_perm_by_str(self):
        add_name_perm = self._create_add_perm()

        self.group.perms.add_perm('field.articles.Article.name.add')

        self.assertTrue(self.group.perms.has_perm(add_name_perm))

        # test perm is correctly available to the user as well
        self.assertFalse(self.user.perms.has_perm(add_name_perm))

        self.user.groups.add(self.group)

        self.assertTrue(self.user.perms.has_perm(add_name_perm))

    def test_fail_add_field_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add_perm('field.articles.Article.name.delete')

    def test_fail_add_field_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.group.perms.add_perm('field.articles.Foo.name.add')

    def test_fail_add_field_perm_non_existent_field_name(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add_perm('field.articles.Article.foo.add')
