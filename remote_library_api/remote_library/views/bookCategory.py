from ..models import Book, Video, BookCategory
from ..serializer import BookSerializer, VideoSerializer, BookCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class BookCategoryAPIView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        bookCategories = BookCategory.objects.all()
        serializer = BookCategorySerializer(bookCategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"bookCategories": []}
        error_response = {"bookCategories": []}
        serializers = []
        request_data = request.data
        required_fields = ["category", "description"]

        for bookCategory in request_data["data"]:
            serializer = BookCategorySerializer(data=bookCategory)

            if list(bookCategory.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"bookCategory": serializer.initial_data}
                response["bookCategories"].append(elem)
            else:
                errors += 1
                elem = {"bookCategory": serializer.initial_data}
                error_response["bookCategories"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class BookCategoryDetailView(APIView):
    def get(self, request, pk, format=None):
        bookCategory = BookCategory.objects.get(pk=pk)
        serializer = BookCategorySerializer(bookCategory)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["category", "description"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = BookCategory.objects.get(pk=pk)
        serializer = BookCategorySerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"bookCategory": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bookCategory = BookCategory.objects.get(pk=pk)
        bookCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
