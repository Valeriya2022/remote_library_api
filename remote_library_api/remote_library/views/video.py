from ..models import Book, Audio, Video, BookCategory
from ..serializer import BookSerializer, AudioSerializer, VideoSerializer, BookCategorySerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.views import APIView
from django.utils.timezone import now


class VideoDetailView(APIView):
    def updateViewsCounter(self, request, pk):
        video = Video.objects.get(pk=pk)
        views = video.views_counter + 1
        request_data = {"views_counter": views}
        serializer = VideoSerializer(video, data=request_data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

    def get(self, request, pk, format=None):
        self.updateViewsCounter(request, pk)
        video = Video.objects.get(pk=pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        allowed_updates = ["name", "author", "description", "source", "url", "path", "publish_date", "video_category"]
        for elem in request.data:
            if not (elem in allowed_updates):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        object = Video.objects.get(pk=pk)
        serializer = VideoSerializer(object, data=request_data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"video": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        video = Video.objects.get(pk=pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoAPIView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request):
        errors = 0
        response = {"videos": []}
        error_response = {"videos": []}
        serializers = []
        request_data = request.data
        required_fields = ["name", "author", "description", "source", "url", "path", "publish_date", "video_category"]

        for video in request_data["data"]:
            serializer = VideoSerializer(data=video)

            if list(video.keys()) == required_fields and serializer.is_valid(raise_exception=False):

                serializers.append(serializer)
                elem = {"video": serializer.initial_data}
                response["videos"].append(elem)
            else:
                errors += 1
                elem = {"video": serializer.initial_data}
                error_response["videos"].append(elem)

        if errors == 0:
            for serial in serializers:
                serial.save()

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)
