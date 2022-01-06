from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'', include(router.urls)),
]
