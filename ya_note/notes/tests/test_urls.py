from django.urls import reverse


class TestURLs:
    SLUG = 'note_slug'
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    LOGIN_URL = reverse('users:login')
    SUCCESS_URL = reverse('notes:success')
    HOME_URL = reverse('notes:home')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')
    EDIT_URL = reverse('notes:edit', args=(SLUG,))
    DELETE_URL = reverse('notes:delete', args=(SLUG,))
    DETAIL_URL = reverse('notes:detail', args=(SLUG,))
