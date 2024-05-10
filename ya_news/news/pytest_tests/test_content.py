from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from .test_urls import TestURLs

User = get_user_model()


class BaseNoteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.client.force_login(cls.author)
        cls.reader_client = Client()
        cls.client.force_login(cls.reader)
        cls.note = cls.create_note()

    def create_note(self, title='Заголовок', text='Текст', slug='slug',
                    author=None):
        if author is None:
            author = self.author
        return Note.objects.create(title=title, text=text, slug=slug,
                                   author=author)

    def test_note_in_list_for_author(self):
        url = TestURLs.LIST_URL
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)
        self.assertEqual(self.note.title, 'Заголовок')
        self.assertEqual(self.note.text, 'Текст')
        self.assertEqual(self.note.author, self.author)

    def test_note_not_in_list_for_another_user(self):
        url = TestURLs.LIST_URL
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_page_contains_form(self):
        urls = {'add': TestURLs.ADD_URL,
                'edit': TestURLs.get_edit_url(self.note.slug)}
        for action, route_name in urls.items():
            with self.subTest(action=action):
                if action == 'add':
                    url = reverse(route_name)
                elif action == 'edit':
                    url = reverse(route_name, args=(self.note.slug,))
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
