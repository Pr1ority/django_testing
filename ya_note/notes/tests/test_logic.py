from http import HTTPStatus

from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note
from .test_base import (BaseNoteTestCase, ADD_URL, LOGIN_URL,
                        SUCCESS_URL, DELETE_URL, EDIT_URL)

User = get_user_model()


class TestNoteCreation(BaseNoteTestCase):
    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(ADD_URL, data=self.form_data)
        expected_url = f'{LOGIN_URL}?next={ADD_URL}'
        self.assertRedirects(response, expected_url)
        self.assertFalse(Note.objects.filter(
            title=self.form_data['title']).exists())

    def test_user_can_create_note(self):
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        created_note = Note.objects.get(id=self.note.id)
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.author, self.author)
        self.assertEqual(created_note.slug, self.form_data['notes_slug'])
        self.assertEqual(Note.objects.filter(
            title=self.form_data['title']).exists(), True)

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
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.title, self.note.title)
        self.assertEqual(note_after.text, self.note.text)
        self.assertEqual(note_after.author, self.note.author)
        self.assertEqual(note_after.slug, self.note.slug)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL,
                                           data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.author, self.note.author)
        self.assertEqual(self.note.slug, self.form_data['notes_slug'])

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
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertFormError(response, 'form', 'slug', errors=(
            self.note.slug + WARNING))
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.text)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('notes_slug')
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.get(title=self.form_data['title'])
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.user)
        self.assertEqual(Note.objects.filter(
            title=self.form_data['title']).exists(), True)
