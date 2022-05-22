import jwt

import remote_library.models
from ..models import Jwt, Book, Video
from ..models import CustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIView
from ..serializer import LoginSerializer, RegisterSerializer, RefreshSerializer, \
    SaveBookSerializer, SaveVideoSerializer, VideoSerializer, BookSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response


def get_random(length):
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, requests):
        serializer = self.serializer_class(data=requests.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['password'])

        user = authenticate(username=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        print("user", user)
        if not user:
            return Response({"error": "Invalid email or password"}, status="400")
        # Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({"some": user.id})
        refresh = get_refresh_token()
        Jwt.objects.create(
            user_id=user.id,
            access=access,
            refresh=refresh
        )
        return Response({"access": access, "refresh": refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"success": "User created."})


def verify_token(token):
    #decode the token
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except Exception:
        return None
    exp=decoded_data["exp"]
    if datetime.now().timestamp() > exp:
        return None
    return decoded_data


class RefreshView(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        access = get_access_token({"some": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()
        return Response({"access": access, "refresh": refresh})


class LogOut(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        Jwt.objects.filter(refresh=active_jwt.refresh).delete()
        return Response({"status": "Successfully logged out"})


class SaveBook(APIView):
    serializer_class = SaveBookSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id=active_jwt.user.id
        book_id = serializer.validated_data["book_id"]
        book_custom_user = Book.saved_by.through
        new_book_user = book_custom_user(book_id=book_id, customuser_id=id)
        new_book_user.save()
        return Response({"status": "Success"})


class SaveVideo(APIView):
    serializer_class = SaveVideoSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id=active_jwt.user.id
        video_id = serializer.validated_data["video_id"]
        video_custom_user = Video.saved_by.through
        new_video_user = video_custom_user(video_id=video_id, customuser_id=id)
        new_video_user.save()
        return Response({"status": "Success"})


class SavedVideosView(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id=active_jwt.user.id
        video_custom_user = Video.saved_by.through
        videos = video_custom_user.objects.filter(customuser_id=id)
        data = []
        for video in videos:
            print(video.video_id)
            video_object = Video.objects.get(pk=video.video_id)
            video_serializer = VideoSerializer(video_object)
            data.append(video_serializer.data)
        return Response(data)


class SavedBooksView(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id=active_jwt.user.id
        book_custom_user = Book.saved_by.through
        books = book_custom_user.objects.filter(customuser_id=id)
        data = []
        for book in books:
            print(book.book_id)
            book_object = Video.objects.get(pk=book.book_id)
            book_serializer = BookSerializer(book_object)
            data.append(book_serializer.data)
        return Response(data)


class VerifySavedBook(APIView):
    serializer_class = SaveBookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id = active_jwt.user.id
        book_id = serializer.validated_data["book_id"]
        book_custom_user = Book.saved_by.through
        book = book_custom_user.objects.filter(book_id=book_id, customuser_id=id)
        print(len(book))
        if (len(book)>=1):
            return Response({"saved": 1})
        else:
            return Response({"saved": 0})


class VerifySavedVideo(APIView):
    serializer_class = SaveVideoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"}, status="400")
        id = active_jwt.user.id
        video_id = serializer.validated_data["video_id"]
        video_custom_user = Video.saved_by.through
        video = video_custom_user.objects.filter(video_id=video_id, customuser_id=id)
        print(len(video))
        if (len(video)>=1):
            return Response({"saved": 1})
        else:
            return Response({"saved": 0})




