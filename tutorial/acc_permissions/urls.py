from django.urls import path, include
from rest_framework import routers

from .api import views


# register viewsets via router.
router = routers.DefaultRouter()
router.register(r'admins', views.AdminViewSet)
router.register(r'matchmakers', views.MatchmakersViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'permissions', views.PermissionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # url(r'^matchmakers/permissions/(?P<pk>[0-9]+)/$', views.MatchmakerPermissions.as_view())
]
