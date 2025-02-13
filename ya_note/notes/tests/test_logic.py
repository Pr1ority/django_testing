from http import HTTPStatus

from pytils.translit import slugify
from django.contrib.auth import get_user_model

from notes.forms import WARNING
from notes.models import Note
from .test_base import (BaseNoteTestCase, ADD_URL, LOGIN_URL,
                        SUCCESS_URL, DELETE_URL, EDIT_URL)

User = get_user_model()


class TestNoteCreation(BaseNoteTestCase):
    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.values_list('id', flat=True))
        response = self.client.post(ADD_URL, data=self.form_data)
        expected_url = f'{LOGIN_URL}?next={ADD_URL}'
        self.assertRedirects(response, expected_url)
        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_after, notes_before)

    def test_user_can_create_note(self):
        notes_before = set(Note.objects.values_list('id', flat=True))
        self.form_data['slug'] = 'new-slug-for-note'
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(len(notes_after) - len(notes_before), 1)
        new_note_id = (notes_after - notes_before).pop()
        new_note = Note.objects.get(id=new_note_id)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.user)
        self.assertEqual(new_note.slug, self.form_data['slug'])

    def test_author_can_delete_note(self):
        note_count_before = Note.objects.count()
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        note_count_after = Note.objects.count()
        self.assertEqual(note_count_after, note_count_before - 1)
        note_exists = Note.objects.filter(id=self.note.id).exists()
        self.assertFalse(note_exists)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(DELETE_URL)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.title, self.note.title)
        self.assertEqual(note_after.text, self.note.text)
        self.assertEqual(note_after.author, self.note.author)
        self.assertEqual(note_after.slug, self.note.slug)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_edit_note(self):
        self.form_data['slug'] = 'new-slug-for-note'
        response = self.author_client.post(EDIT_URL,
                                           data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.author, self.note.author)
        self.assertEqual(updated_note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(EDIT_URL,
                                           data=self.form_data)
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(note_after.text, self.note.text)
        self.assertEqual(note_after.title, self.note.title)
        self.assertEqual(note_after.author, self.note.author)
        self.assertEqual(note_after.slug, self.note.slug)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        notes_before = set(Note.objects.values_list('id', flat=True))
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertFormError(response, 'form', 'slug', errors=(
            self.note.slug + WARNING))
        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_after, notes_before)

    def test_empty_slug(self):
        notes_before = set(Note.objects.values_list('id', flat=True))
        self.form_data.pop('notes_slug')
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(len(notes_after) - len(notes_before), 1)
        new_note_id = (notes_after - notes_before).pop()
        new_note = Note.objects.get(id=new_note_id)
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.user)
