from rest_framework import permissions


class IsUserAssociatedWithWallet(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is associated with the wallet of the income instance
        return request.user in obj.wallet.users.all()


class IsUserAssociatedWithWalletDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is associated with the wallet
        return request.user in obj.users.all()