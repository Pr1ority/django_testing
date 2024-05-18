from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from pytest_django.asserts import assertRedirects


User = get_user_model()

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
REDIRECT_EDIT_URL = pytest.lazy_fixture('redirect_edit_url')
REDIRECT_DELETE_URL = pytest.lazy_fixture('redirect_delete_url')
CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT,
         HTTPStatus.NOT_FOUND),
        (DELETE_URL, NOT_AUTHOR_CLIENT,
         HTTPStatus.NOT_FOUND),
    ),
)
def test_availability_for_comment_edit_and_delete(client_fixture,
                                                  expected_status, url):
    response = client_fixture.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url_fixture',
    [
        (EDIT_URL, REDIRECT_EDIT_URL),
        (DELETE_URL, REDIRECT_DELETE_URL),
    ],
)
def test_redirect_for_anonymous_client(url, redirect_url_fixture, client):
    response = client.get(url)
    assertRedirects(response, redirect_url_fixture)
