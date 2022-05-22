from django.urls import path
from rest_framework.authtoken import views
from .views import \
    BookAPIView, \
    VideoAPIView, \
    BookDetailView, \
    VideoDetailView,\
    BookCategoryAPIView,\
    VideoCategoryAPIView,\
    BookCategoryDetailView,\
    VideoCategoryDetailView,\
    GovernmentalResourceAPIView,\
    GovernmentalResourceDetailView,\
    GovernmentalResourceCategoryAPIView,\
    GovernmentalResourceCategoryDetailView,\
    AuthorAPIView,\
    AuthorDetailView,\
    LoginView,\
    RegisterView,\
    BookPopularView,\
    VideoPopularView,\
    GovResourcesPopularView,\
    RefreshView,\
    SearchedMaterialAPIView,\
    SearchedMaterialDetailView,\
    LogOut,\
    SaveBook,\
    SaveVideo,\
    SavedVideosView,\
    SavedBooksView,\
    VerifySavedBook,\
    VerifySavedVideo

urlpatterns = [
    path('books', BookAPIView.as_view(), name="books"),
    path('books/<int:pk>', BookDetailView.as_view(), name="books"),
    path('books-popular', BookPopularView.as_view(), name="popular books"),
    path('videos', VideoAPIView.as_view(), name="videos"),
    path('videos/<int:pk>', VideoDetailView.as_view(), name="videos"),
    path('videos-popular', VideoPopularView.as_view(), name="popular videos"),
    path('book-category', BookCategoryAPIView.as_view(), name="book-category"),
    path('book-category/<int:pk>', BookCategoryDetailView.as_view(), name="book category"),
    path('video-category', VideoCategoryAPIView.as_view(), name="video-category"),
    path('video-category/<int:pk>', VideoCategoryDetailView.as_view(), name="video category"),
    path('governmental-resource', GovernmentalResourceAPIView.as_view(), name="governmental resource"),
    path('governmental-resource-popular', GovResourcesPopularView.as_view(), name="governmental resource popular"),
    path('governmental-resource/<int:pk>', GovernmentalResourceDetailView.as_view(), name="governmental resource"),
    path('governmental-resource-category', GovernmentalResourceCategoryAPIView.as_view(), name="governmental-resource-category"),
    path('governmental-resource-category/<int:pk>', GovernmentalResourceCategoryDetailView.as_view(), name="governmental resource category"),
    path('authors', AuthorAPIView.as_view(), name="authors"),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name="authors"),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('searched-materials', SearchedMaterialAPIView.as_view(), name="searched materials"),
    path('searched-materials/<int:pk>', SearchedMaterialDetailView.as_view(), name="searched material"),
    path('logout', LogOut.as_view(), name="Log out"),
    path('save-book', SaveBook.as_view(), name="Save Book"),
    path('save-video', SaveVideo.as_view(), name="Save Video"),
    path('get-saved-videos', SavedVideosView.as_view(), name="Saved videos view"),
    path('get-saved-books', SavedBooksView.as_view(), name="Saved books view"),
    path('verify-saved-book', VerifySavedBook.as_view(), name="Verify saved book"),
    path('verify-saved-video', VerifySavedVideo.as_view(), name="Verify saved video")
]
