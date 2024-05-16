from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from notes.models import Note

User = get_user_model()



SLUG = 'note_slug'
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
LOGIN_URL = reverse('users:login')
SUCCESS_URL = reverse('notes:success')
HOME_URL = reverse('notes:home')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

class TestURLs:
    EDIT_URL = reverse('notes:edit', args=(SLUG,))
    DELETE_URL = reverse('notes:delete', args=(SLUG,))
    DETAIL_URL = reverse('notes:detail', args=(SLUG,))


class BaseNoteTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create(username='Автор')
        self.reader = User.objects.create(username='Читатель')
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.reader_client = Client()
        self.reader_client.force_login(self.reader)
        self.note = Note.objects.create(title='Заголовок', text='Текст',
                                        slug='notes_slug', author=self.author)
        self.user = User.objects.create(username='Пользователь')
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
        self.form_data = {'title': 'Заголовок',
                          'text': 'Текст',
                          'notes_slug': 'notes_slug'}

