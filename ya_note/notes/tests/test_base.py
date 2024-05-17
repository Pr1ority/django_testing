from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from notes.models import Note

User = get_user_model()


SLUG = 'notes_slug'
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


class BaseNoteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(title='Заголовок', text='Текст',
                                       slug=SLUG, author=cls.author)
        cls.user = User.objects.create(username='Пользователь')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'title': 'Заголовок',
                         'text': 'Текст',
                         'notes_slug': SLUG}
