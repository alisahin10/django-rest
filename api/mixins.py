from .permissions import IsStaffEditorPermission
from rest_framework import permissions


class StafEditorPermisisonMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

"""
class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data = [self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)
"""

class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user

        # If staff is allowed to view all, return the queryset without filtering
        if self.allow_staff_view and user.is_staff:
            return qs

        # Otherwise, filter the queryset based on the user
        lookup_data = {self.user_field: user}
        return qs.filter(**lookup_data)


