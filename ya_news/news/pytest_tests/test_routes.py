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


@pytest.mark.parametrize(
    'url',
    (
        HOME_URL,
        DETAIL_URL,
        LOGIN_URL,
        LOGOUT_URL,
        SIGNUP_URL,
    ),
)
def test_pages_availability(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status, url',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND,
         EDIT_URL),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND,
         DELETE_URL),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK, EDIT_URL),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK, DELETE_URL),
    ),
)
def test_availability_for_comment_edit_and_delete(parametrized_client,
                                                  expected_status, url,
                                                  comment):
    if comment is None:
        pytest.skip

    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        EDIT_URL,
        DELETE_URL,
    ),
)
def test_redirect_for_anonymous_client(url, client, comment):
    login_url = LOGIN_URL
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
