from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .test_urls import TestURLs
from .test_content import BaseNoteTestCase

User = get_user_model()


class TestRoutes(BaseNoteTestCase):
    def setUp(self):
        super().setUp()

    def test_status_codes(self):
        urls = (
            TestURLs.HOME_URL,
            TestURLs.LOGIN_URL,
            TestURLs.LOGOUT_URL,
            TestURLs.SIGNUP_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        cases = [
            (TestURLs.get_edit_url(self, self.note.slug), self.author_client,
             HTTPStatus.OK),
            (TestURLs.get_delete_url(self, self.note.slug), self.author_client,
             HTTPStatus.OK),
            (TestURLs.get_detail_url(self.note.slug), self.author_client,
             HTTPStatus.OK),
            (TestURLs.get_edit_url(self.note.slug), self.reader_client,
             HTTPStatus.NOT_FOUND),
            (TestURLs.get_delete_url(self.note.slug), self.reader_client,
             HTTPStatus.NOT_FOUND),
            (TestURLs.get_detail_url(self.note.slug), self.reader_client,
             HTTPStatus.NOT_FOUND),
        ]
        for url, client, expected_status in cases:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (TestURLs.get_edit_url(self, self.note.slug), ),
            (TestURLs.get_delete_url(self, self.note.slug), ),
            (TestURLs.LIST_URL, None),
            (TestURLs.SUCCESS_URL, None),
            (TestURLs.ADD_URL, None),
            (TestURLs.get_detail_url(self.note.slug), ),
        )
        for url, args in urls:
            with self.subTest(url=url):
                if args is not None:
                    url = reverse(url, args=(args,))
                response = self.client.get(url)
                redirect_url = f'{TestURLs.LOGIN_URL}?next={url}'
                self.assertRedirects(response, redirect_url)
