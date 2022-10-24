from django.urls import path, include
from rest_framework import routers

from .views import LinkViewSet, redirect_url_view, index

router = routers.DefaultRouter()
router.register("links", LinkViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("redirect/<str:shortened_part>/", redirect_url_view, name="redirect"),
    path("", index, name="index"),
]

app_name = "shortener"
