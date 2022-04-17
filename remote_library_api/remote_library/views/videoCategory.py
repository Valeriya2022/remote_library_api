from ..models import Book, Video, BookCategory, VideoCategory
from ..serializer import BookSerializer, VideoSerializer, BookCategorySerializer, VideoCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class VideoCategoryAPIView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        videoCategories = VideoCategory.objects.all()
        serializer = VideoCategorySerializer(videoCategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"videoCategories": []}
        error_response = {"videoCategories": []}
        serializers = []
        request_data = request.data
        required_fields = ["category", "description"]

        for videoCategory in request_data["data"]:
            serializer = VideoCategorySerializer(data=videoCategory)

            if list(videoCategory.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"videoCategory": serializer.initial_data}
                response["videoCategories"].append(elem)
            else:
                errors += 1
                elem = {"videoCategory": serializer.initial_data}
                error_response["videoCategories"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class VideoCategoryDetailView(APIView):
    def get(self, request, pk, format=None):
        videoCategory = VideoCategory.objects.get(pk=pk)
        serializer = VideoCategorySerializer(videoCategory)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["category", "description"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = VideoCategory.objects.get(pk=pk)
        serializer = VideoCategorySerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"videoCategory": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        videoCategory = VideoCategory.objects.get(pk=pk)
        videoCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)