from django_perms.models import Perm

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase


class ModelPermTestCaseMixin:

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


class ModelPermTestCase(ModelPermTestCaseMixin, ArticleTestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_model_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.model_perms().get())


class ArticleUserModelPermPermTestCase(ModelPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_model_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created model perm
        self.assertEquals(perm, self.user.perms.all().get())

    def test_add_model_perm_by_str(self):
        add_perm = self._create_add_perm()

        self.user.perms.add('model.articles.Article.add')

        # test the new user perm is the created add model perm
        self.assertEquals(add_perm, self.user.perms.all().get())

    def test_fail_add_model_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('model.articles.Article.delete')

    def test_fail_add_model_perm_by_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.user.perms.add('model.articles.Bar.fap')

    def test_has_model_perm(self):
        add_perm = self._create_add_perm()

        self.user.perms.add(add_perm)

        self.assertTrue(self.user.perms.has_perm('model.articles.Article.add'))


class ArticleGroupModelPermPermTestCase(ModelPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_model_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new user perm is the created model perm
        self.assertEquals(perm, self.group.perms.all().get())

    def test_add_model_perm_by_str(self):
        add_perm = self._create_add_perm()

        self.group.perms.add('model.articles.Article.add')

        # test the new user perm is the created add model perm
        self.assertEquals(add_perm, self.group.perms.all().get())

    def test_fail_add_model_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('model.articles.Article.delete')

    def test_fail_add_model_perm_non_existent_model(self):
        self._create_perm()
        with self.assertRaises(LookupError):
            self.group.perms.add('model.articles.Bar.fap')
