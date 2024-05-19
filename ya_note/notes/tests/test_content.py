from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from .test_base import BaseNoteTestCase, LIST_URL, ADD_URL, EDIT_URL

User = get_user_model()


class TestContent(BaseNoteTestCase):
    def test_note_in_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        note_from_list = notes.get(id=self.note.id)
        self.assertEqual(note_from_list.title, self.note.title)
        self.assertEqual(note_from_list.text, self.note.text)
        self.assertEqual(note_from_list.author, self.note.author)
        self.assertEqual(note_from_list.slug, self.note.slug)

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_form_on_pages(self):
        urls = [
            ADD_URL,
            EDIT_URL
        ]

        for url in urls:
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
