from django_perms.models import Perm

from articles.models import Article

from .base import ArticleTestCase, ArticleUserPermTestCase, ArticleGroupPermTestCase
from .factories import ArticleFactory


class ObjectPermTestCaseMixin:

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


class ObjectPermTestCase(ObjectPermTestCaseMixin, ArticleTestCase):

    def setUp(self):
        super().setUp()
        self.article = Article.objects.create(name='foo', text='foo foo')
        self.article2 = Article.objects.create(name='bar', text='bar bar')

    def test_perm_has_correct_type(self):
        perm = self._create_perm()
        self.assertTrue(perm.is_object_perm)

    def test_perm_is_in_correct_queryset_filter(self):
        perm = self._create_perm()
        self.assertEquals(perm, Perm.objects.object_perms().get())


class ArticleUserObjectPermPermTestCase(ObjectPermTestCaseMixin, ArticleUserPermTestCase):

    def setUp(self):
        super().setUp()
        self.article = ArticleFactory()
        self.article2 = ArticleFactory()

    def test_add_object_perm_by_perm(self):
        perm = self._create_perm()

        self.user.perms.add(perm)

        # test the new user perm is the created object perm
        self.assertEquals(perm, self.user.perms.all().get())

    def test_add_object_perm_by_codename_and_object(self):
        add_obj_perm = self._create_add_perm()

        self.user.perms.add('add', obj=self.article)

        # test the new user perm is the created add object perm
        self.assertEquals(add_obj_perm, self.user.perms.all().get())

    def test_fail_add_object_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('delete', model=Article)

    def test_fail_add_object_perm_by_non_existent_object(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.user.perms.add('add', obj=self.article2)

    def test_has_object_perm(self):
        add_obj_perm = self._create_add_perm()

        self.user.perms.add(add_obj_perm)

        self.assertTrue(self.user.perms.has_perm('object.articles.Article.add', self.article))


class ArticleGroupObjectPermPermTestCase(ObjectPermTestCaseMixin, ArticleGroupPermTestCase):

    def setUp(self):
        super().setUp()
        self.article = Article.objects.create(name='foo', text='foo foo')
        self.article2 = Article.objects.create(name='bar', text='bar bar')

    def test_add_object_perm_by_perm(self):
        perm = self._create_perm()

        self.group.perms.add(perm)

        # test the new user perm is the created object perm
        self.assertEquals(perm, self.group.perms.all().get())

    def test_add_object_perm_by_codename_and_object(self):
        add_obj_perm = self._create_add_perm()

        self.group.perms.add('add', obj=self.article)

        # test the new user perm is the created add object perm
        self.assertEquals(add_obj_perm, self.group.perms.all().get())

    def test_fail_add_object_perm_by_non_existent_codename(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('delete', model=Article)

    def test_fail_add_object_perm_by_non_existent_object(self):
        self._create_perm()
        with self.assertRaises(Perm.DoesNotExist):
            self.group.perms.add('add', obj=self.article2)
