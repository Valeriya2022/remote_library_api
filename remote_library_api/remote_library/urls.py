from django.urls import path
from .views import \
    BookAPIView, \
    AudioAPIView,\
    VideoAPIView, \
    BookDetailView, \
    AudioDetailView,\
    VideoDetailView,\
    BookCategoryAPIView,\
    AudioCategoryAPIView,\
    VideoCategoryAPIView,\
    BookCategoryDetailView,\
    AudioCategoryDetailView,\
    VideoCategoryDetailView,\
    GovernmentalResourceAPIView,\
    GovernmentalResourceDetailView,\
    GovernmentalResourceCategoryAPIView,\
    GovernmentalResourceCategoryDetailView,\
    AuthorAPIView,\
    AuthorDetailView

urlpatterns = [
    path('books', BookAPIView.as_view(), name="books"),
    path('books/<int:pk>', BookDetailView.as_view(), name="books"),
    path('audios', AudioAPIView.as_view(), name="audios"),
    path('audios/<int:pk>', AudioDetailView.as_view(), name="audios"),
    path('videos', VideoAPIView.as_view(), name="videos"),
    path('videos/<int:pk>', VideoDetailView.as_view(), name="videos"),
    path('book-category', BookCategoryAPIView.as_view(), name="book-category"),
    path('book-category/<int:pk>', BookCategoryDetailView.as_view(), name="book category"),
    path('audio-category', AudioCategoryAPIView.as_view(), name="audio-category"),
    path('audio-category/<int:pk>', AudioCategoryDetailView.as_view(), name="audio category"),
    path('video-category', VideoCategoryAPIView.as_view(), name="video-category"),
    path('video-category/<int:pk>', VideoCategoryDetailView.as_view(), name="video category"),
    path('governmental-resource', GovernmentalResourceAPIView.as_view(), name="governmental resource"),
    path('governmental-resource/<int:pk>', GovernmentalResourceDetailView.as_view(), name="governmental resource"),
    path('governmental-resource-category', GovernmentalResourceCategoryAPIView.as_view(), name="governmental resource category"),
    path('governmental-resource-category/<int:pk>', GovernmentalResourceCategoryDetailView.as_view(), name="governmental resource category"),
    path('authors', AuthorAPIView.as_view(), name="authors"),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name="authors"),
]