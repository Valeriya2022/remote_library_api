from rest_framework import status

from ..models import SearchedMaterial
from ..serializer import SearchedMaterialSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class SearchedMaterialAPIView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all book categories.
        """
        searchedMaterial = SearchedMaterial.objects.all()
        serializer = SearchedMaterialSerializer(searchedMaterial, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"searchedMaterials": []}
        error_response = {"searchedMaterials": []}
        serializers = []
        request_data = request.data
        required_fields = ["query", "category"]

        for searchedMaterial in request_data["data"]:
            serializer = SearchedMaterialSerializer(data=searchedMaterial)

            if list(searchedMaterial.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"searchedMaterials": serializer.initial_data}
                response["searchedMaterials"].append(elem)
            else:
                errors += 1
                elem = {"searchedMaterials": serializer.initial_data}
                error_response["searchedMaterials"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)


class SearchedMaterialDetailView(APIView):
    def delete(self, request, pk, format=None):
        searchedMaterial = SearchedMaterial.objects.get(pk=pk)

        searchedMaterial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
