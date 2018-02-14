from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^Permission/~create/$",
        view=views.PermissionCreateView.as_view(),
        name='Permission_create',
    ),
    url(
        regex="^Permission/(?P<pk>\d+)/~delete/$",
        view=views.PermissionDeleteView.as_view(),
        name='Permission_delete',
    ),
    url(
        regex="^Permission/(?P<pk>\d+)/$",
        view=views.PermissionDetailView.as_view(),
        name='Permission_detail',
    ),
    url(
        regex="^Permission/(?P<pk>\d+)/~update/$",
        view=views.PermissionUpdateView.as_view(),
        name='Permission_update',
    ),
    url(
        regex="^Permission/$",
        view=views.PermissionListView.as_view(),
        name='Permission_list',
    ),
]
