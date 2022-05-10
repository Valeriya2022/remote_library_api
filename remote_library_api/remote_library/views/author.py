from ..models import Book, Author
from ..serializer import BookSerializer, AuthorSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class AuthorDetailView(APIView):
    def get(self, request, pk, format=None):
        book = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(book)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["first_name", "last_name", "description", "books"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"author": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorAPIView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"authors": []}
        error_response = {"authors": []}
        serializers = []
        request_data = request.data
        required_fields = ["first_name", "last_name", "description", "books"]

        for author in request_data["data"]:
            serializer = AuthorSerializer(data=author)
            if list(author.keys()) == required_fields and serializer.is_valid(raise_exception=True):

                serializers.append(serializer)
                elem = {"author": serializer.initial_data}
                response["authors"].append(elem)
            else:
                errors += 1
                elem = {"author": serializer.initial_data}
                error_response["authors"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)
