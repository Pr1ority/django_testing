from django.urls import reverse


class TestURLs:
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    LOGIN_URL = reverse('users:login')
    SUCCESS_URL = reverse('note:success')
    HOME_URL = reverse('notes:home')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')

    def get_edit_url(slug):
        return reverse('notes:edit', args=[slug])

    def get_delete_url(slug):
        return reverse('notes:delete', args=[slug])

    def get_detail_url(slug):
        return reverse('notes:detail', args=[slug])
