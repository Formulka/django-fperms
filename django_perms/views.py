from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Permission,
)


class PermissionCreateView(CreateView):

    model = Permission


class PermissionDeleteView(DeleteView):

    model = Permission


class PermissionDetailView(DetailView):

    model = Permission


class PermissionUpdateView(UpdateView):

    model = Permission


class PermissionListView(ListView):

    model = Permission

