from fperms import get_perm_model
from django.test import TestCase, override_settings

from .base import ArticleUserPermTestCase, ArticleGroupPermTestCase
from .factories import GroupFactory, UserFactory

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

        self.user.fperms.add_perm(perm)

        self.assertTrue(self.user.fperms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.user.fperms.add_perm('generic.export')

        self.assertTrue(self.user.fperms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.user.fperms.add_perm('generic.export')

    @override_settings(PERM_AUTO_CREATE=True)
    def test_auto_create_generic_perm(self):
        self.user.fperms.add_perm('generic.export')

    @override_settings(PERM_AUTO_CREATE=True)
    def test_clear_perms(self):
        self.user.fperms.add_perm('generic.export')
        self.user.fperms.add_perm('generic.foo')
        self.user.fperms.add_perm('generic.bar')
        self.user.fperms.add_perm('generic.baz')

        self.assertEquals(self.user.fperms.all().count(), 4)

        self.user.fperms.clear()

        self.assertEquals(self.user.fperms.all().count(), 0)

    @override_settings(PERM_AUTO_CREATE=True)
    def test_remove_generic_perm_by_codename(self):
        self.user.fperms.add_perm('generic.export')
        self.assertTrue(self.user.fperms.has_perm('generic.export'))

        self.user.fperms.remove_perm('generic.export')
        self.assertFalse(self.user.fperms.has_perm('generic.export'))

    @override_settings(PERM_AUTO_CREATE=True)
    def test_remove_generic_perm_by_perm(self):
        export_perm = self._create_perm()

        self.user.fperms.add_perm(export_perm)
        self.assertTrue(self.user.fperms.has_perm(export_perm))

        self.user.fperms.remove_perm(export_perm)
        self.assertFalse(self.user.fperms.has_perm(export_perm))

    def test_has_generic_perm_from_wildcard(self):
        self._create_perm_wildcard()

        self.user.fperms.add_perm('generic.*')

        self.assertTrue(self.user.fperms.has_perm('generic.whatever'))

    def test_has_generic_perm_from_being_superuser(self):
        self._create_perm_wildcard()

        self.user.is_superuser = True
        self.user.save()

        self.assertTrue(self.user.fperms.has_perm('generic.whatever'))


class ArticleGroupGenericPermPermTestCase(GenericPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_generic_perm_by_perm(self):
        perm = self._create_perm()

        self.group.fperms.add_perm(perm)

        # test the new group perm is the created generic perm
        self.assertTrue(self.group.fperms.has_perm(perm))

    def test_add_generic_perm_by_codename(self):
        export_perm = self._create_perm()

        self.group.fperms.add_perm('generic.export')

        self.assertTrue(self.group.fperms.has_perm(export_perm))

        # test perm is correctly available to the user as well
        self.assertFalse(self.user.fperms.has_perm(export_perm))

        self.user.fgroups.add(self.group)

        self.assertTrue(self.user.fperms.has_perm(export_perm))

    def test_fail_add_generic_perm_non_existent_codename(self):
        with self.assertRaises(Perm.DoesNotExist):
            self.group.fperms.add_perm('generic.export')

    def test_subgroup_permissions_should_be_evaluated_for_specific_level(self):
        export_perm = self._create_perm()
        second_group = GroupFactory()
        second_group.fperms.add(export_perm)

        self.group.fgroups.add(second_group)
        self.user.fgroups.add(self.group)
        self.assertTrue(self.user.fperms.has_perm(export_perm))

        with override_settings(PERM_GROUP_MAX_LEVEL=0):
            self.assertFalse(self.user.fperms.has_perm(export_perm))

        with override_settings(PERM_GROUP_MAX_LEVEL=3):
            self.assertTrue(self.user.fperms.has_perm(export_perm))

    def test_group_cycles_should_be_correctly_evaluated(self):
        export_perm = self._create_perm()
        second_group = GroupFactory()
        second_group.fperms.add(export_perm)

        self.group.fgroups.add(second_group)
        second_group.fgroups.add(self.group)
        self.user.fgroups.add(self.group)

        self.assertTrue(self.user.fperms.has_perm(export_perm))
