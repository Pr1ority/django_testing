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
             HTTPStatus.OK, 'Author'),
            (DELETE_URL, self.author_client,
             HTTPStatus.OK, 'Author'),
            (DETAIL_URL, self.author_client,
             HTTPStatus.OK, 'Author'),
            (EDIT_URL, self.reader_client,
             HTTPStatus.NOT_FOUND, 'Reader'),
            (DELETE_URL, self.reader_client,
             HTTPStatus.NOT_FOUND, 'Reader'),
            (DETAIL_URL, self.reader_client,
             HTTPStatus.NOT_FOUND, 'Reader'),
            (HOME_URL, self.client,
             HTTPStatus.OK, None),
            (LOGIN_URL, self.client,
             HTTPStatus.OK, None),
            (LOGOUT_URL, self.client,
             HTTPStatus.OK, None),
            (SIGNUP_URL, self.client,
             HTTPStatus.OK, None),
            (ADD_URL, self.reader_client, HTTPStatus.OK, None),
            (LIST_URL, self.reader_client, HTTPStatus.OK, None),
            (SUCCESS_URL, self.reader_client, HTTPStatus.OK, None),
        ]
        for url, client, expected_status, role in cases:
            with self.subTest(url=url, role=role):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status,
                                 f'Failed for {role} client at URL: {url}')

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
