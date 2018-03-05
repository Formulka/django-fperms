from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

User = get_user_model()


DEFAULT_PASSWORD = 'foofoobar'


class UserFactory(factory.DjangoModelFactory):

    username = factory.LazyAttribute(lambda a: '{0}'.format(a.last_name).lower())

    first_name = factory.Sequence(lambda n: 'John{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Doe{0}'.format(n))
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    password = DEFAULT_PASSWORD

    is_active = True

    class Meta:
        model = User
        django_get_or_create = ('username',)


class GroupFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'Group{0}'.format(n))

    class Meta:
        model = 'auth.Group'


class ArticleFactory(factory.DjangoModelFactory):

    name = fuzzy.FuzzyText()
    text = fuzzy.FuzzyText()

    class Meta:
        model = 'articles.Article'
