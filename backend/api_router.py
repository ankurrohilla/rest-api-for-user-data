from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = router.urls

api_urls = [
    path("", include(('users.urls', 'users'), namespace='users')),

]
urlpatterns += api_urls
