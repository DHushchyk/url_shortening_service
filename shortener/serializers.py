from rest_framework import serializers

from shortener.models import Shortener, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "count"]


class ShortenerListSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    redirect_link = serializers.CharField(read_only=True)

    class Meta:
        model = Shortener
        fields = ["id", "original_url", "short_url", "redirect_link"]


class ShortenerDetailSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Shortener
        fields = [
            "id",
            "original_url",
            "short_url",
            "redirect_link",
            "redirect_count",
            "last_redirect_time",
            "countries"
        ]
