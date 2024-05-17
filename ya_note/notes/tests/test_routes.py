from http import HTTPStatus

from django.contrib.auth import get_user_model

from .test_base import (TestURLs, BaseNoteTestCase, LIST_URL, ADD_URL,
                        LOGIN_URL, SUCCESS_URL, HOME_URL, LOGOUT_URL,
                        SIGNUP_URL)

User = get_user_model()


class TestRoutes(BaseNoteTestCase):
    def test_status_codes(self):
        cases = [
            (TestURLs.EDIT_URL, self.author_client,
             HTTPStatus.OK),
            (TestURLs.DELETE_URL, self.author_client,
             HTTPStatus.OK),
            (TestURLs.DETAIL_URL, self.author_client,
             HTTPStatus.OK),
            (TestURLs.EDIT_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (TestURLs.DELETE_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (TestURLs.DETAIL_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (HOME_URL, self.client,
             HTTPStatus.OK),
            (LOGIN_URL, self.client,
             HTTPStatus.OK),
            (LOGOUT_URL, self.client,
             HTTPStatus.OK),
            (SIGNUP_URL, self.client,
             HTTPStatus.OK),
        ]
        for url, client, expected_status in cases:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (TestURLs.EDIT_URL),
            (TestURLs.DELETE_URL),
            (LIST_URL),
            (SUCCESS_URL),
            (ADD_URL),
            (TestURLs.DETAIL_URL),
        )
        for url in urls:
            redirect_url = f'{LOGIN_URL}?next={url}'
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
