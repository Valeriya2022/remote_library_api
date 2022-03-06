from ..models import BookCategory, GovernmentalResource
from ..serializer import BookCategorySerializer, GovernmentalResourceSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class GovernmentalResourceAPIView(APIView):
    def get(self, request, format=None):
        governmentalResource = GovernmentalResource.objects.all()
        serializer = GovernmentalResourceSerializer(governmentalResource, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"governmentalResources": []}
        error_response = {"governmentalResources": []}
        serializers = []
        request_data = request.data
        required_fields = ["source", "url", "path", "category"]

        for governmentalResource in request_data["data"]:
            serializer = GovernmentalResourceSerializer(data=governmentalResource)

            if list(governmentalResource.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"governmentalResource": serializer.initial_data}
                response["governmentalResources"].append(elem)
            else:
                errors += 1
                elem = {"governmentalResource": serializer.initial_data}
                error_response["governmentalResources"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class GovernmentalResourceDetailView(APIView):
    def updateViewsCounter(self, request, pk):
        governmentalResource = GovernmentalResource.objects.get(pk=pk)
        views = governmentalResource.views_counter + 1
        request_data = {"views_counter": views}
        serializer = GovernmentalResourceSerializer(governmentalResource, data=request_data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

    def get(self, request, pk, format=None):
        self.updateViewsCounter(request, pk)
        governmentalResource = GovernmentalResource.objects.get(pk=pk)
        serializer = GovernmentalResourceSerializer(governmentalResource)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["source", "url", "path", "category"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = GovernmentalResource.objects.get(pk=pk)
        serializer = GovernmentalResourceSerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"governmentalResource": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        governmentalResource = GovernmentalResource.objects.get(pk=pk)
        governmentalResource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
