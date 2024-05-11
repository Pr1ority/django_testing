from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from .test_urls import TestURLs

User = get_user_model()


class BaseNoteTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create(username='Автор')
        self.reader = User.objects.create(username='Читатель')
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.reader_client = Client()
        self.reader_client.force_login(self.reader)
        self.note = self.create_note()

    def create_note(self, title='Заголовок', text='Текст', slug='notes_slug',
                    author=None):
        if author is None:
            author = self.author
        return Note.objects.create(title=title, text=text, slug=slug,
                                   author=author)

    def test_note_in_list_for_author(self):
        url = TestURLs.LIST_URL
        response = self.author_client.get(url)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        self.assertEqual(self.note.title, 'Заголовок')
        self.assertEqual(self.note.text, 'Текст')
        self.assertEqual(self.note.author, self.author)

    def test_note_not_in_list_for_another_user(self):
        url = TestURLs.LIST_URL
        response = self.reader_client.get(url)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_note_page_contains_form(self):
        urls = [
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        ]
        self.client.force_login(self.author)
        for url_name, args in urls:
            url = reverse(url_name, args=args)
            response = self.client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
