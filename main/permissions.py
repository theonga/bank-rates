from rest_framework import permissions

class IsBankManager(permissions.BasePermission):
    """
    Custom permission to only allow bank managers to create, update, or delete branches and exchange rates.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a bank manager
        return request.user.is_authenticated and request.user.user_type == 'bank_admin'

class IsBranchManager(permissions.BasePermission):
    """
    Custom permission to only allow branch managers to create, update, or delete branches and exchange rates.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a branch manager
        return request.user.is_authenticated and request.user.user_type == 'branch_manager'

class IsBankManagerForBranch(permissions.BasePermission):
    """
    Custom permission to only allow the bank manager of the bank associated with the branch to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the manager of the bank associated with the branch
        return request.user.is_authenticated and obj.bank.manager == request.user