from django.urls import reverse


class TestURLs:
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    LOGIN_URL = reverse('users:login')
    SUCCESS_URL = reverse('notes:success')
    HOME_URL = reverse('notes:home')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')
    EDIT_URL = reverse('notes:edit', args=['slug'])
    DELETE_URL = reverse('notes:edit', args=['slug'])
    DETAIL_URL = reverse('notes:edit', args=['slug'])