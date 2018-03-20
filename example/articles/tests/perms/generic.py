from fperms import get_perm_model
from django.test import TestCase

from .base import ArticleUserPermTestCase, ArticleGroupPermTestCase


Perm = get_perm_model()


class GenericPermTestCaseMixin:

    def _create_perm(self):
        return Perm.objects.create(
            codename='export',
        )

    def _create_perm_wildcard(self):
        return Perm.objects.create(
            codename='*',
        )


class GenericPermTestCase(GenericPermTestCaseMixin, TestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_generic_perm())


class ArticleUserGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        self.assertTrue(self.user.perms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.user.perms.add('generic.export')

        self.assertTrue(self.user.perms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('generic.export')

    def test_has_generic_perm_from_wildcard(self):
        self._create_perm_wildcard()

        self.user.perms.add('generic.*')

        self.assertTrue(self.user.perms.has_perm('generic.whatever'))


class ArticleGroupGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new group perm is the created generic perm
        self.assertTrue(self.group.perms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.group.perms.add('generic.export')

        self.assertTrue(self.group.perms.has_perm(export_perm))

        # test perm is correctly available to the user as well
        self.assertFalse(self.user.perms.has_perm(export_perm))

        self.user.groups.add(self.group)

        self.assertTrue(self.user.perms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('generic.export')
