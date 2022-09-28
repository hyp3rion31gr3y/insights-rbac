#
# Copyright 2022 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Views for OCM/integrations API."""

import logging

from django.db.models import Q
from django_filters import rest_framework as filters
from internal.integration.serializers import TenantSerializer
from management.cache import TenantCache
from management.filters import CommonFilters
from management.group.view import GroupViewSet
from management.permissions.admin_access import AdminAccessPermission
from management.role.view import RoleViewSet
from rest_framework import mixins, viewsets

from api.models import Tenant


logger = logging.getLogger(__name__)
TENANTS = TenantCache()


def groups(request, org_id):
    """Format and pass internal groups request to /groups/ API."""
    view = GroupViewSet.as_view({"get": "list"})
    return view(request)


def roles(request, org_id):
    """Format and pass internal roles request to /roles/ API."""
    view = RoleViewSet.as_view({"get": "list"})
    return view(request)


def groups_for_principal(request, org_id, principals):
    """Format and pass /principal/<username>/groups/ request to /groups/ API."""
    view = GroupViewSet.as_view({"get": "list"})
    return view(request, principals=principals)


def roles_for_group(request, org_id, uuid):
    """Pass internal /groups/<uuid>/roles/ request to /groups/ API."""
    view = GroupViewSet.as_view({"get": "roles"})
    return view(request, uuid=uuid)


def roles_for_group_principal(request, org_id, principals, uuid):
    """Pass internal /principal/<username>/groups/<uuid>/roles/ request to /groups/ API."""
    view = GroupViewSet.as_view({"get": "roles"})
    return view(request, uuid=uuid, principals=principals)


def principals_for_group(request, org_id, uuid):
    """Pass internal /groups/<uuid>/principals/ request to /groups/ API."""
    view = GroupViewSet.as_view({"get": "principals"})
    return view(request, uuid=uuid)


class TenantFilter(CommonFilters):
    """Filter for tenant."""

    def modified_only_filter(self, queryset, field, modified_only):
        """Filter to return only modified tenants."""
        if modified_only:
            queryset = (
                queryset.filter(Q(group__system=False) | Q(role__system=False))
                .prefetch_related("group_set", "role_set")
                .distinct()
            )
        return queryset

    modified_only = filters.BooleanFilter(field_name="modified_only", method="modified_only_filter")


class TenantViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Tenant view set."""

    queryset = Tenant.objects.all()
    permission_classes = (AdminAccessPermission,)
    serializer_class = TenantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TenantFilter

    def list(self, request, *args, **kwargs):
        """Tenant list."""
        return super().list(request=request, args=args, kwargs=kwargs)
