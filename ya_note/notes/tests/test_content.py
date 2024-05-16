from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from .test_base import BaseNoteTestCase, LIST_URL

User = get_user_model()


class TestContent(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_note_in_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.text)
        self.assertContains(response, self.note.author)

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_form_on_pages(self):
        pages = {
            'add': reverse('notes:add'),
            'edit': reverse('notes:edit', args=(self.note.slug,))
        }

        for page_name, url in pages.items():
            with self.subTest(page_name=page_name):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
