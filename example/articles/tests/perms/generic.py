from fperms import get_perm_model
from django.test import TestCase, override_settings

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

        self.user.perms.add_perm(perm)

        self.assertTrue(self.user.perms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.user.perms.add_perm('generic.export')

        self.assertTrue(self.user.perms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add_perm('generic.export')

    @override_settings(PERM_AUTO_CREATE=True)
    def test_auto_create_generic_perm(self):
        self.user.perms.add_perm('generic.export')

    @override_settings(PERM_AUTO_CREATE=True)
    def test_clear_perms(self):
        self.user.perms.add_perm('generic.export')
        self.user.perms.add_perm('generic.foo')
        self.user.perms.add_perm('generic.bar')
        self.user.perms.add_perm('generic.baz')

        self.assertEquals(self.user.perms.all().count(), 4)

        self.user.perms.clear()

        self.assertEquals(self.user.perms.all().count(), 0)

    @override_settings(PERM_AUTO_CREATE=True)
    def test_remove_generic_perm_by_codename(self):
        self.user.perms.add_perm('generic.export')
        self.assertTrue(self.user.perms.has_perm('generic.export'))

        self.user.perms.remove_perm('generic.export')
        self.assertFalse(self.user.perms.has_perm('generic.export'))

    @override_settings(PERM_AUTO_CREATE=True)
    def test_remove_generic_perm_by_perm(self):
        export_perm = self._create_perm()

        self.user.perms.add_perm(export_perm)
        self.assertTrue(self.user.perms.has_perm(export_perm))

        self.user.perms.remove_perm(export_perm)
        self.assertFalse(self.user.perms.has_perm(export_perm))

    def test_has_generic_perm_from_wildcard(self):
        self._create_perm_wildcard()

        self.user.perms.add_perm('generic.*')

        self.assertTrue(self.user.perms.has_perm('generic.whatever'))

    def test_has_generic_perm_from_being_superuser(self):
        self._create_perm_wildcard()

        self.user.is_superuser = True
        self.user.save()

        self.assertTrue(self.user.perms.has_perm('generic.whatever'))


class ArticleGroupGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add_perm(perm)

        # test the new group perm is the created generic perm
        self.assertTrue(self.group.perms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.group.perms.add_perm('generic.export')

        self.assertTrue(self.group.perms.has_perm(export_perm))

        # test perm is correctly available to the user as well
        self.assertFalse(self.user.perms.has_perm(export_perm))

        self.user.groups.add(self.group)

        self.assertTrue(self.user.perms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add_perm('generic.export')
