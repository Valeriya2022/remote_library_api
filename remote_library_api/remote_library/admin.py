from django.contrib import admin

from remote_library.models import \
    Book,\
    Video, \
    Audio,\
    Author,\
    GovernmentalResource,\
    GovernmentalResourceCategory,\
    VideoCategory,\
    AudioCategory,\
    BookCategory


admin.site.register(Book)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Author)
admin.site.register(GovernmentalResource)
admin.site.register(GovernmentalResourceCategory)
admin.site.register(BookCategory)
admin.site.register(AudioCategory)
admin.site.register(VideoCategory)
