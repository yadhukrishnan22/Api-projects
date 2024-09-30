from rest_framework.permissions import BasePermission

#custom persmission

class OwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

