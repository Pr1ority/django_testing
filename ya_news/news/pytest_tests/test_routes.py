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
REDIRECT_URL = pytest.lazy_fixture('redirect_url')

@pytest.mark.parametrize(
    'url, client, expected_status',
    (
        (HOME_URL, None, HTTPStatus.OK),
        (DETAIL_URL, None, HTTPStatus.OK),
        (LOGIN_URL, None, HTTPStatus.OK),
        (LOGOUT_URL, None, HTTPStatus.OK),
        (SIGNUP_URL, None, HTTPStatus.OK),
        (EDIT_URL, pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (DELETE_URL, pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (EDIT_URL, pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (DELETE_URL, pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
def test_availability_for_comment_edit_and_delete(client,
                                                  expected_status, url):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        EDIT_URL,
        DELETE_URL,
    ),
)
def test_redirect_for_anonymous_client(url, client, redirect_url):
    expected_redirect_url = redirect_url(url)
    response = client.get(url)
    assertRedirects(response, expected_redirect_url)
