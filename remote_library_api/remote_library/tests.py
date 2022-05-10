from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework import status
from .models import BookCategory, VideoCategory, GovernmentalResourceCategory, Book

class BookCategoryTests(APITestCase):
    def test_create_book_category(self):
        """
        Ensure we can create a new book category object.
        """
        url = reverse('book-category')
        data = {'data': [{'category': 'Maths'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookCategory.objects.count(), 1)
        self.assertEqual(BookCategory.objects.get().category, 'Maths')

    # def test_create_book(self):
    #     """
    #     Ensure we can create a new book object.
    #     """
    #
    #     url = reverse('books')
    #     data = {'data': [{'name': 'Book', 'description': 'Test Description', 'source': 'many Books',
    #                       'path': 'http://localhost:4000/books/Round-the-Fire-Stories.pdf',
    #                       'url': 'http://localhost:4000/books/Round-the-Fire-Stories.pdf',
    #                       'publish_year': 1234, 'book_category': 1}]}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Book.objects.count(), 1)
    #     self.assertEqual(Book.objects.get().name, 'Book')


class VideoCategoryTests(APITestCase):
    def test_create_video_category(self):
        """
        Ensure we can create a new video category object.
        """
        url = reverse('video-category')
        data = {'data': [{'category': 'Maths'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VideoCategory.objects.count(), 1)
        self.assertEqual(VideoCategory.objects.get().category, 'Maths')

class GovResourceCategoryTests(APITestCase):
    def test_create_video_category(self):
        """
        Ensure we can create a new governmental resource category object.
        """
        url = reverse('governmental-resource-category')
        data = {'data': [{'category': 'News'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GovernmentalResourceCategory.objects.count(), 1)
        self.assertEqual(GovernmentalResourceCategory.objects.get().category, 'News')

