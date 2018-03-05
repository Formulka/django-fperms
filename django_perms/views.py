from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from django_perms.conf import settings


class PermissionCreateView(CreateView):

    model = settings.PERM_MODEL


class PermissionDeleteView(DeleteView):

    model = settings.PERM_MODEL


class PermissionDetailView(DetailView):

    model = settings.PERM_MODEL


class PermissionUpdateView(UpdateView):

    model = settings.PERM_MODEL


class PermissionListView(ListView):

    model = settings.PERM_MODEL

