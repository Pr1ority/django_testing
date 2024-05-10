from http import HTTPStatus

from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note
from .test_urls import TestURLs
from .test_content import BaseNoteTestCase

User = get_user_model()


class TestNoteCreation(BaseNoteTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='Пользователь')
        self.url = TestURLs.ADD_URL
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
        self.form_data = {'title': 'Заголовок',
                          'text': 'Текст',
                          'slug': 'slug'}
        self.edit_url = TestURLs.get_edit_url(self, self.note.slug)
        self.delete_url = TestURLs.get_delete_url(self.note.slug)
        self.notes_url = TestURLs.LIST_URL

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.url, data=self.form_data)
        login_url = TestURLs.LOGIN_URL
        expected_url = f'{login_url}?next={self.url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.filter(
            title=self.form_data['title']).exists(), False)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.filter(
            title=self.form_data['title']).exists(), True)
        note = Note.objects.first()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.user)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_author_can_delete_note(self):
        url = TestURLs.SUCCESS_URL
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, url)
        note_exists = Note.objects.filter(slug=self.note.slug).exists()
        self.assertFalse(note_exists)

    def test_user_cant_delete_note_of_another_user(self):
        note_before = Note.objects.get(slug=self.note.slug)
        response = self.reader_client.delete(self.delete_url)
        note_after = Note.objects.get(slug=self.note.slug)
        self.assertEqual(note_after.title, note_before.title)
        self.assertEqual(note_after.text, note_before.text)
        self.assertEqual(note_after.author, note_before.author)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, TestURLs.SUCCESS_URL)
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.author, self.user)
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.note.text, self.note.text)
        self.assertEqual(self.note.title, self.note.title)
        self.assertEqual(self.note.author, self.note.author)
        self.assertEqual(self.note.slug, self.note.slug)

    def test_not_unique_slug(self):
        url = TestURLs.ADD_URL
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(url, data=self.form_data)
        self.assertFormError(response, 'form', 'slug', errors=(
            self.note.slug + WARNING))
        self.assertEqual(self.note.text, self.note.text)
        self.assertEqual(self.note.title, self.note.title)
        self.assertEqual(self.note.author, self.note.author)
        self.assertEqual(self.note.slug, self.note.slug)

    def test_empty_slug(self):
        url = TestURLs.ADD_URL
        self.form_data.pop('slug')
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, TestURLs.SUCCESS_URL)
        self.assertEqual(Note.objects.filter(
            title=self.form_data['title']).exists(), True)
        new_note = Note.objects.first()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.user)
