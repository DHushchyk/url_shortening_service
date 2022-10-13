from random import choice

from string import ascii_letters, digits


SIZE = 6

AVAILABLE_CHARS = ascii_letters + digits + "-"


def create_random_code(chars=AVAILABLE_CHARS):
    """Creates a random string with the predetermined size"""

    return "".join([choice(chars) for _ in range(SIZE)])


def create_shortened_url(model_instance):
    """Creates a shortened url and checks if it is unique"""

    shortened_url = create_random_code()

    model_class = model_instance.__class__

    if model_class.objects.filter(short_url=shortened_url).exists():

        return create_shortened_url(model_instance)

    return shortened_url


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
