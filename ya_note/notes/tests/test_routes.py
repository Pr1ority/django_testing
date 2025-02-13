from http import HTTPStatus

from django.contrib.auth import get_user_model

from .test_base import (BaseNoteTestCase, LIST_URL, ADD_URL,
                        LOGIN_URL, SUCCESS_URL, HOME_URL, LOGOUT_URL,
                        SIGNUP_URL, EDIT_URL, DELETE_URL, DETAIL_URL)

User = get_user_model()


class TestRoutes(BaseNoteTestCase):
    def test_status_codes(self):
        cases = [
            (EDIT_URL, self.author_client,
             HTTPStatus.OK),
            (DELETE_URL, self.author_client,
             HTTPStatus.OK),
            (DETAIL_URL, self.author_client,
             HTTPStatus.OK),
            (EDIT_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (DETAIL_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (HOME_URL, self.client,
             HTTPStatus.OK),
            (LOGIN_URL, self.client,
             HTTPStatus.OK),
            (LOGOUT_URL, self.client,
             HTTPStatus.OK),
            (SIGNUP_URL, self.client,
             HTTPStatus.OK),
            (ADD_URL, self.reader_client, HTTPStatus.OK),
            (LIST_URL, self.reader_client, HTTPStatus.OK),
            (SUCCESS_URL, self.reader_client, HTTPStatus.OK),
        ]
        for url, client, expected_status in cases:
            with self.subTest(url=url, client=client):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status,
                                 f'Failed for {client} client at URL: {url}')

    def test_redirect_for_anonymous_client(self):
        urls = (
            EDIT_URL,
            DELETE_URL,
            LIST_URL,
            SUCCESS_URL,
            ADD_URL,
            DETAIL_URL,
        )
        redirect_urls = {url: f'{LOGIN_URL}?next={url}' for url in urls}
        for url, redirect_url in redirect_urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
