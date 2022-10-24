from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.test.client import Client
from rest_framework.test import APIClient

from shortener.models import Shortener

from shortener.serializers import ShortenerListSerializer

BASE_URL = "http://127.0.0.1:8000/"
LINKS_URL = urljoin(BASE_URL, "api/links/")
ORIGINAL_URL_SAMPLE = "https://www.django-rest-framework.org/"


def create_sample_link(client, url=ORIGINAL_URL_SAMPLE):
    payload = {"original_url": url}

    return client.post(LINKS_URL, payload)


def create_few_links(client, ids):
    for i in range(ids):
        payload = {"original_url": f"{ORIGINAL_URL_SAMPLE}{i}/"}
        client.post(LINKS_URL, payload)


def get_detail_url(link):
    link_id = link.data["id"]
    return f"{LINKS_URL}{link_id}/"


class UnAuthenticatedShortenerAPITest(TestCase):
    def setUp(self):
        self.client = Client(REMOTE_ADDR="212.90.60.68")
        self.second_client = Client(REMOTE_ADDR="2.58.194.134")  # Netherlands

    def test_create_link(self):

        res = create_sample_link(self.client)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_link_already_exists(self):
        create_sample_link(self.client)
        res = create_sample_link(self.client)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_links(self):
        create_few_links(self.client, 4)
        create_sample_link(self.second_client)
        res = self.client.get(LINKS_URL)

        links = Shortener.objects.all()
        serializer = ShortenerListSerializer(links, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_link_detail_access(self):
        first_link = create_sample_link(self.client)

        second_link = create_sample_link(self.second_client, "https://football.ua/")

        first_res = self.client.get(get_detail_url(first_link))
        second_res = self.client.get(get_detail_url(second_link))

        self.assertEqual(first_res.status_code, status.HTTP_200_OK)
        self.assertEqual(second_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_link(self):
        first_link = create_sample_link(self.client)

        create_sample_link(self.client, "https://football.ua/")
        links_before_delete = Shortener.objects.count()

        res_delete = self.client.delete(get_detail_url(first_link))

        links = Shortener.objects.filter(is_deleted=False)
        serializer = ShortenerListSerializer(links, many=True)

        res_list = self.client.get(LINKS_URL)

        links_after_delete = Shortener.objects.count()

        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res_list.data, serializer.data)
        self.assertEqual(links_before_delete, links_after_delete)

    def test_redirect_url_statistics(self):
        link = create_sample_link(self.client, "https://football.ua/")
        redirect_url = link.data["redirect_link"]
        detail_url = get_detail_url(link)
        self.third_client = Client(REMOTE_ADDR="107.181.177.135")  # Canada
        self.fourth_client = Client(REMOTE_ADDR="12.58.194.137")  # USA
        for _ in range(5):
            self.client.get(redirect_url)
        for _ in range(3):
            self.second_client.get(redirect_url)
        for _ in range(2):
            self.third_client.get(redirect_url)
        self.fourth_client.get(redirect_url)

        expected_countries = [
            "Ukraine: 5 times.",
            "Netherlands: 3 times.",
            "Canada: 2 times.",
        ]

        res = self.client.get(detail_url)

        self.assertEqual(res.data["redirect_count"], 11)
        self.assertEqual(res.data["Top 3 countries redirect"], expected_countries)


class AuthenticatedShortenerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_create_link(self):

        res = create_sample_link(self.client)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list_links(self):
        self.second_client = Client(REMOTE_ADDR="107.181.177.135")
        create_few_links(self.client, 4)
        create_sample_link(self.second_client)
        res = self.client.get(LINKS_URL)

        links = Shortener.objects.all()
        serializer = ShortenerListSerializer(links, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
