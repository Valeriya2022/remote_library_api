from rest_framework import serializers


from .models import \
    Book,\
    Video, \
    Author,\
    GovernmentalResource,\
    GovernmentalResourceCategory,\
    VideoCategory,\
    BookCategory

#
# class AudioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Audio
#         fields = '__all__'



class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


# class AudioCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AudioCategory
#         fields = '__all__'


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'


class GovernmentalResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentalResource
        fields = '__all__'


class GovernmentalResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentalResourceCategory
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "description", "books")


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ("id", "name", "description", "source", "path",
                  "url", "upload_date_time", "last_visited_date_time",
                  "publish_year", "views_counter", "book_category", "authors", "saved_by")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()





