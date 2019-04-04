from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsSuperAdmin
from .serializers import GroupSerializer, PermissionSerializer, UserSerializer


UserModel = get_user_model()


class MatchmakersViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows matchmakers to be viewed or edited(groups and permissions).
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = UserModel.objects.filter(is_matchmaker=True)
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        u = request.pop('id')
        user = UserModel.objects.get(id=u)
        permissions_data = request.pop('user_permissions')
        groups_data = request.pop('groups')
        for p in permissions_data:
            user.user_permissions.add(p)
        for g in groups_data:
            user.groups.add(g)
        return Response(user, status=status.HTTP_200_OK)


class AdminViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows admins to be viewed or edited(groups and permissions).
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = UserModel.objects.filter(is_admin=True)
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        u = request.pop('id')
        user = UserModel.objects.get(id=u)
        permissions_data = request.pop('user_permissions')
        groups_data = request.pop('groups')
        for p in permissions_data:
            user.user_permissions.add(p)
        for g in groups_data:
            user.groups.add(g)
        return Response(user, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperAdmin]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows permissions to be viewed or edited.
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperAdmin]
