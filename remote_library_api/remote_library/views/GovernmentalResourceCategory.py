from ..models import BookCategory, GovernmentalResource, GovernmentalResourceCategory
from ..serializer import BookCategorySerializer, GovernmentalResourceSerializer, GovernmentalResourceCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class GovernmentalResourceCategoryAPIView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        governmentalResourceCategory = GovernmentalResourceCategory.objects.all()
        serializer = GovernmentalResourceCategorySerializer(governmentalResourceCategory, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"governmentalResourceCategories": []}
        error_response = {"governmentalResourceCategories": []}
        serializers = []
        request_data = request.data
        required_fields = ["category", "description"]

        for governmentalResourceCategory in request_data["data"]:
            serializer = GovernmentalResourceCategorySerializer(data=governmentalResourceCategory)

            if list(governmentalResourceCategory.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"governmentalResourceCategory": serializer.initial_data}
                response["governmentalResourceCategories"].append(elem)
            else:
                errors += 1
                elem = {"governmentalResourceCategory": serializer.initial_data}
                error_response["governmentalResourceCategories"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class GovernmentalResourceCategoryDetailView(APIView):
    def get(self, request, pk, format=None):
        governmentalResource = GovernmentalResourceCategory.objects.get(pk=pk)
        serializer = GovernmentalResourceCategorySerializer(governmentalResource)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["category", "description"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = GovernmentalResourceCategory.objects.get(pk=pk)
        serializer = GovernmentalResourceCategorySerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"governmentalResource": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        governmentalResourceCategory = GovernmentalResourceCategory.objects.get(pk=pk)
        governmentalResourceCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

