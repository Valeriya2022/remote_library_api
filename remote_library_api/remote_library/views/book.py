from ..models import Book, Video, BookCategory
from ..serializer import BookSerializer, VideoSerializer, BookCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now

class BookPopularView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        books = Book.objects.all()
        if len(books) > 5:
            popular_books = sorted(books, key=lambda x: x.views_counter, reverse=True)
            serializer = BookSerializer(popular_books[0:5], many=True)
            return Response(serializer.data)
        else:
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

class BookDetailView(APIView):
    def updateViewsCounter(self, request, pk):
        book = Book.objects.get(pk=pk)
        views = book.views_counter + 1
        request_data = {"views_counter": views}
        serializer = BookSerializer(book, data=request_data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

    def get(self, request, pk, format=None):
        self.updateViewsCounter(request, pk)
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["name", "description", "source", "path", "url", "publish_year", "book_category", "saved_by"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = Book.objects.get(pk=pk)
        serializer = BookSerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"book": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookAPIView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"books": []}
        error_response = {"books": []}
        serializers = []
        request_data = request.data
        print("data", request_data)
        required_fields = ["name", "description", "source", "path", "url", "publish_year", "book_category"]

        for book in request_data["data"]:
            serializer = BookSerializer(data=book)
            if list(book.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"book": serializer.initial_data}
                response["books"].append(elem)
            else:
                errors += 1
                elem = {"book": serializer.initial_data}
                error_response["books"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)
