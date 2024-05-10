from django.urls import reverse


class TestURLs:
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    LOGIN_URL = reverse('users:login')
    SUCCESS_URL = reverse('notes:success')
    HOME_URL = reverse('notes:home')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')

    def get_edit_url(self, slug):
        return reverse('notes:edit', kwargs={'slug': slug})

    def get_delete_url(self, slug):
        return reverse('notes:delete', kwargs={'slug': slug})

    def get_detail_url(self, slug):
        return reverse('notes:detail', args=[slug])
