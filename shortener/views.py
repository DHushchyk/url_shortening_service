from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Shortener
from .serializers import ShortenerListSerializer, ShortenerDetailSerializer
from .utils import get_client_ip


class LinkViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShortenerListSerializer
        if self.action == "retrieve":
            return ShortenerDetailSerializer
        return ShortenerListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.queryset.filter(
                owner=self.request.user
            ).filter(is_deleted=False)
        else:
            queryset = self.queryset.filter(
                ip=get_client_ip(self.request)
            ).filter(is_deleted=False)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        serializer.save(ip=get_client_ip(self.request))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


def redirect_url_view(request, shortened_part):
    shortener = get_object_or_404(Shortener, short_url=shortened_part)
    shortener.redirect_count += 1
    shortener.last_redirect_time = datetime.now()
    shortener.save()

    return HttpResponseRedirect(shortener.original_url)
