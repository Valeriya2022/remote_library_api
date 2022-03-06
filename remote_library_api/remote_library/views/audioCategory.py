from ..models import Book, Audio, Video, BookCategory, AudioCategory
from ..serializer import BookSerializer, AudioSerializer, VideoSerializer, BookCategorySerializer, AudioCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class AudioCategoryAPIView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        audioCategories = AudioCategory.objects.all()
        serializer = AudioCategorySerializer(audioCategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"audioCategories": []}
        error_response = {"audioCategories": []}
        serializers = []
        request_data = request.data
        required_fields = ["category", "description"]

        for audioCategory in request_data["data"]:
            serializer = AudioCategorySerializer(data=audioCategory)

            if list(audioCategory.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"audioCategory": serializer.initial_data}
                response["audioCategories"].append(elem)
            else:
                errors += 1
                elem = {"audioCategory": serializer.initial_data}
                error_response["audioCategories"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class AudioCategoryDetailView(APIView):
    def get(self, request, pk, format=None):
        audioCategory = AudioCategory.objects.get(pk=pk)
        serializer = AudioCategorySerializer(audioCategory)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["category", "description"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = AudioCategory.objects.get(pk=pk)
        serializer = AudioCategorySerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"audioCategory": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        audioCategory = AudioCategory.objects.get(pk=pk)
        audioCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

