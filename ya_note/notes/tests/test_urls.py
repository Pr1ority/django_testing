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

    def __init__(self, slug):
        self.slug = slug
        self.EDIT_URL = reverse('notes:edit', args=(self.slug,))
        self.DELETE_URL = reverse('notes:delete', args=(self.slug,))
        self.DETAIL_URL = reverse('notes:detail', args=(self.slug,))
