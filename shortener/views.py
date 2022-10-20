from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status

from rest_framework.response import Response


from .models import Shortener, Country
from .serializers import ShortenerListSerializer, ShortenerDetailSerializer
from .utils import get_client_ip, create_redirect_url, create_shortened_url, add_redirect_country


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = serializer.data
        countries = [
            str(country) for country in Country.objects.filter(link=instance.id)[:3]
        ]
        if countries:
            response[f"Top {len(countries)} countries"] = countries
        return Response(response)

    def get_queryset(self):
        queryset = self.queryset.filter(is_deleted=False)
        if self.action == "retrieve":
            if self.request.user.is_authenticated:
                queryset = queryset.filter(owner=self.request.user)
            else:
                queryset = queryset.filter(ip=get_client_ip(self.request))
            return queryset
        return queryset

    def perform_create(self, serializer):
        short_url = create_shortened_url()
        redirect_url = create_redirect_url(short_url, self.request)
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        serializer.save(
            ip=get_client_ip(self.request),
            short_url=short_url,
            redirect_link=redirect_url
        )

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
    add_redirect_country(request, shortener.id)

    return HttpResponseRedirect(shortener.original_url)
