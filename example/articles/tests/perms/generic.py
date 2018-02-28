from django_perms.models import Perm
from django.test import TestCase

from .base import ArticleUserPermTestCase, ArticleGroupPermTestCase


class GenericPermTestCaseMixin:

    def _create_perm(self):
        return Perm.objects.create(
            codename='export',
        )


class GenericPermTestCase(GenericPermTestCaseMixin, TestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_generic_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.generic_perms().get())


class ArticleUserGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created generic perm
        self.assertEquals(perm, self.user.perms.all().get())

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.user.perms.add('generic.export')

        # test the new user perm is the created export generic perm
        self.assertEquals(export_perm, self.user.perms.all().get())

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('generic.export')

    def test_has_generic_perm(self):
        export_perm = self._create_perm()

        self.user.perms.add(export_perm)

        self.assertTrue(self.user.perms.has_perm('generic.export'))


class ArticleGroupGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new user perm is the created generic perm
        self.assertEquals(perm, self.group.perms.all().get())

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.group.perms.add('generic.export')

        # test the new user perm is the created export generic perm
        self.assertEquals(export_perm, self.group.perms.all().get())

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('generic.export')

    def test_has_generic_perm(self):
        self._create_perm()

        self.group.perms.add('generic.export')

        self.assertTrue(self.group.perms.has_perm('generic.export'))
