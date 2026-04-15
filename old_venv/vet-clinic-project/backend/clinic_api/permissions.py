from rest_framework.permissions import BasePermission

from .models import Profile


class IsVet(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                    getattr(request.user, "profile", None) and 
                    request.user.profile.role == Profile.ROLE_VET)


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                    getattr(request.user, "profile", None) and 
                    request.user.profile.role in (Profile.ROLE_VET, Profile.ROLE_ASSISTANT))


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        prof = getattr(user, "profile", None)
        if prof and prof.role in (Profile.ROLE_VET, Profile.ROLE_ASSISTANT):
            return True
        if hasattr(obj, "owner_id"):
            return obj.owner_id == user.id
        if hasattr(obj, "pet"):
            return obj.pet.owner_id == user.id
        return False
