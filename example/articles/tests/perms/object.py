from django_perms import enums
from django_perms.models import Perm

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase
from .factories import ArticleFactory


class ObjectPermTestCaseMixin:

    def setUp(self):
        super().setUp()
        self.article = ArticleFactory()
        self.article2 = ArticleFactory()

    def _create_perm(self):
        return self._create_add_perm()

    def _create_add_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_OBJECT,
            codename=enums.PERM_CODENAME_ADD,
            content_object=self.article,
        )

    def _create_delete_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_OBJECT,
            codename=enums.PERM_CODENAME_DELETE,
            content_object=self.article,
        )

    def _create_wildcard_perm(self):
        return Perm.objects.create(
            type=enums.PERM_TYPE_OBJECT,
            codename=enums.PERM_CODENAME_WILDCARD,
            content_object=self.article,
        )


class ObjectPermTestCase(ObjectPermTestCaseMixin, ArticleTestCase):

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_object_perm())


class ArticleUserObjectPermPermTestCase(ObjectPermTestCaseMixin, ArticleUserPermTestCase):

    def test_add_object_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created object perm
        self.assertEquals(perm, self.user.perms.all().get())

    def test_add_object_perm_by_str(self):
        add_obj_perm = self._create_add_perm()

        self.user.perms.add('object.articles.Article.add', obj=self.article)

        # test the new user perm is the created add object perm
        self.assertEquals(add_obj_perm, self.user.perms.all().get())

    def test_fail_add_object_perm_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('object.articles.Article.delete', obj=self.article)

    def test_fail_add_object_perm_non_existent_object(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('object.articles.Article.add', obj=self.article2)

    def test_has_object_perm(self):
        add_obj_perm = self._create_add_perm()

        self.user.perms.add(add_obj_perm)

        self.assertTrue(self.user.perms.has_perm('object.articles.Article.add', self.article))

    def test_has_model_perm_from_wildcard(self):
        self._create_wildcard_perm()

        self.user.perms.add('object.articles.Article.*', self.article)

        self.assertTrue(self.user.perms.has_perm('object.articles.Article.whatever', self.article))


class ArticleGroupObjectPermPermTestCase(ObjectPermTestCaseMixin, ArticleGroupPermTestCase):

    def test_add_object_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new user perm is the created object perm
        self.assertEquals(perm, self.group.perms.all().get())

    def test_add_object_perm_by_str(self):
        add_obj_perm = self._create_add_perm()

        self.group.perms.add('object.articles.Article.add', obj=self.article)

        # test the new user perm is the created add object perm
        self.assertEquals(add_obj_perm, self.group.perms.all().get())

    def test_fail_add_object_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('object.articles.Article.delete', obj=self.article)

    def test_fail_add_object_perm_by_non_existent_object(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('object.articles.Article.add', obj=self.article2)
