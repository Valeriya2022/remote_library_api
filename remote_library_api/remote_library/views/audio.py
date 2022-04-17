# from ..models import Book, Audio, Video, BookCategory
# from ..serializer import BookSerializer, AudioSerializer, VideoSerializer, BookCategorySerializer
# from rest_framework.response import Response
# from rest_framework import status, authentication
# from rest_framework.views import APIView
# from django.utils.timezone import now
#
#
# class AudioDetailView(APIView):
#     def updateViewsCounter(self, request, pk):
#         audio = Audio.objects.get(pk=pk)
#         views = audio.views_counter + 1
#         request_data = {"views_counter": views}
#         serializer = AudioSerializer(audio, data=request_data, partial=True)
#         if serializer.is_valid(raise_exception=False):
#             serializer.save()
#
#
#     def get(self, request, pk, format=None):
#         self.updateViewsCounter(request, pk)
#         audio = Audio.objects.get(pk=pk)
#         serializer = AudioSerializer(audio)
#
#         return Response(serializer.data)
#
#     def patch(self, request, pk, format=None):
#         allowed_updates = ["name", "author", "description", "source", "url", "path", "publish_date", "audio_category", "saved_by"]
#         for elem in request.data:
#             if not (elem in allowed_updates):
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#         request_data = request.data
#         object = Audio.objects.get(pk=pk)
#         serializer = AudioSerializer(object, data=request_data, partial=True)
#
#         if serializer.is_valid(raise_exception=False):
#             serializer.save()
#             return Response({"audio": serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         audio = Audio.objects.get(pk=pk)
#         audio.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
# class AudioAPIView(APIView):
#     """
#     View to list all users in the system.
#
#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         audios = Audio.objects.all()
#         serializer = AudioSerializer(audios, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         errors = 0
#         response = {"audios": []}
#         error_response = {"audios": []}
#         serializers = []
#         request_data = request.data
#         required_fields = ["name", "author","transcript", "source", "url", "path", "publish_date", "audio_category"]
#
#         for audio in request_data["data"]:
#             serializer = AudioSerializer(data=audio)
#
#             if list(audio.keys()) == required_fields and serializer.is_valid(raise_exception=False):
#
#                 serializers.append(serializer)
#                 elem = {"audio": serializer.initial_data}
#                 response["audios"].append(elem)
#             else:
#                 errors += 1
#                 elem = {"audio": serializer.initial_data}
#                 error_response["audios"].append(elem)
#
#         if errors == 0:
#             for serial in serializers:
#                 serial.save()
#
#             return Response(response, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"validation error": error_response}, status=status.HTTP_400_BAD_REQUEST)