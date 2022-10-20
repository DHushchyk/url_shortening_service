from random import choice

from string import ascii_letters, digits
from django.contrib.sites.shortcuts import get_current_site

from .models import Shortener

SIZE = 6

AVAILABLE_CHARS = ascii_letters + digits + "-"


def create_random_code(chars=AVAILABLE_CHARS):
    """Creates a random string with the predetermined size"""

    return "".join([choice(chars) for _ in range(SIZE)])


def create_shortened_url():
    """Creates a shortened url and checks if it is unique"""

    shortened_url = create_random_code()

    if Shortener.objects.filter(short_url=shortened_url).exists():

        return create_shortened_url()

    return shortened_url


def create_redirect_url(short_part, request):
    """Creates a redirect url"""

    current_site = get_current_site(request)

    return f"http://{current_site}/redirect/{short_part}/"


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
