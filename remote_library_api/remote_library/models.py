from django.db import models
from django.utils.timezone import now
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



class AudioCategory(models.Model):
    category = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category


class BookCategory(models.Model):
    category = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category


class VideoCategory(models.Model):
    category = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1000)
    path = models.FilePathField(path=BASE_DIR / "remote_library/projectMaterials/books", match=None, recursive=False, max_length=100)
    url = models.URLField(null=True)
    upload_date_time = models.DateTimeField(default=now, editable=False)
    last_visited_date_time = models.DateTimeField(default=now)
    publish_year = models.PositiveIntegerField(null=True, blank=True)
    views_counter = models.PositiveIntegerField(default=0)
    book_category = models.ForeignKey(BookCategory, null=True, on_delete=models.CASCADE)

    def __str__(self):
        authors = self.authors.all()
        author_names = ""
        # for author in authors:
        #     author_names += author.first_name + " " + author.last_name
        return self.name + "by" + str(authors)


class Video(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1000)
    url = models.URLField(null=True)
    path = models.FilePathField(path=BASE_DIR / "remote_library/projectMaterials/videos", match=None, recursive=False, max_length=100)
    upload_date_time = models.DateTimeField(default=now, editable=False)
    last_visited_date_time = models.DateTimeField(default=now)
    publish_date = models.PositiveIntegerField(null=True, blank=True)
    views_counter = models.PositiveIntegerField(default=0)
    video_category = models.ForeignKey(VideoCategory, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Audio(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=1000, blank=True, null=True)
    transcript = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=1000)
    url = models.URLField(null=True)
    path = models.FilePathField(path=BASE_DIR / "remote_library/projectMaterials/audios", match=None, recursive=False, max_length=100)
    upload_date_time = models.DateTimeField(default=now, editable=False)
    last_visited_date_time = models.DateTimeField(default=now)
    publish_date = models.PositiveIntegerField(null=True, blank=True)
    views_counter = models.PositiveIntegerField(default=0)
    audio_category = models.ForeignKey(AudioCategory, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    books = models.ManyToManyField(Book, related_name="authors", blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class GovernmentalResourceCategory(models.Model):
    category = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category


class GovernmentalResource(models.Model):
    source = models.CharField(max_length=1000)
    url = models.URLField(null=True)
    update_date = models.DateField(auto_now=True)
    path = models.FilePathField(path=BASE_DIR / "remote_library/projectMaterials/governmental_resources",
    max_length=200, allow_folders=True)
    category = models.ForeignKey(GovernmentalResourceCategory, on_delete=models.CASCADE)
    views_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.source

