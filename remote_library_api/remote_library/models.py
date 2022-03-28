from django.db import models
from django.utils.timezone import now
from pathlib import Path
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
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
    path = models.FilePathField(path="C:/Users/valeriya.nikiforova/Documents/UCA/Senior/FYP/remote_library_web/remote-library/public/projectMaterials/books", match=None, recursive=False, max_length=100)
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
    path = models.FilePathField(path="C:/Users/valeriya.nikiforova/Documents/UCA/Senior/FYP/remote_library_web/remote-library/public/projectMaterials/videos", match=None, recursive=False, max_length=100)
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
    path = models.FilePathField(path="C:/Users/valeriya.nikiforova/Documents/UCA/Senior/FYP/remote_library_web/remote-library/public/projectMaterials/videos", match=None, recursive=False, max_length=100)
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


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser mast have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser mast have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Jwt(models.Model):
    user = models.ForeignKey(CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
