from django.contrib import admin

from remote_library.models import \
    Book,\
    Video, \
    Author,\
    GovernmentalResource,\
    GovernmentalResourceCategory,\
    VideoCategory,\
    BookCategory,\
    CustomUser, \
    Jwt


admin.site.register(Book)
admin.site.register(Video)
admin.site.register(Author)
admin.site.register(GovernmentalResource)
admin.site.register(GovernmentalResourceCategory)
admin.site.register(BookCategory)
admin.site.register(VideoCategory)
admin.site.register(CustomUser)
admin.site.register(Jwt)
