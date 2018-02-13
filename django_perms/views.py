# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Permission,
    ModelPermission,
    FieldPermission,
    SlugPermission,
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


class ModelPermissionCreateView(CreateView):

    model = ModelPermission


class ModelPermissionDeleteView(DeleteView):

    model = ModelPermission


class ModelPermissionDetailView(DetailView):

    model = ModelPermission


class ModelPermissionUpdateView(UpdateView):

    model = ModelPermission


class ModelPermissionListView(ListView):

    model = ModelPermission


class FieldPermissionCreateView(CreateView):

    model = FieldPermission


class FieldPermissionDeleteView(DeleteView):

    model = FieldPermission


class FieldPermissionDetailView(DetailView):

    model = FieldPermission


class FieldPermissionUpdateView(UpdateView):

    model = FieldPermission


class FieldPermissionListView(ListView):

    model = FieldPermission


class SlugPermissionCreateView(CreateView):

    model = SlugPermission


class SlugPermissionDeleteView(DeleteView):

    model = SlugPermission


class SlugPermissionDetailView(DetailView):

    model = SlugPermission


class SlugPermissionUpdateView(UpdateView):

    model = SlugPermission


class SlugPermissionListView(ListView):

    model = SlugPermission

