from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from django_perms.models import Perm


class PermissionCreateView(CreateView):

    model = Perm


class PermissionDeleteView(DeleteView):

    model = Perm


class PermissionDetailView(DetailView):

    model = Perm


class PermissionUpdateView(UpdateView):

    model = Perm


class PermissionListView(ListView):

    model = Perm

