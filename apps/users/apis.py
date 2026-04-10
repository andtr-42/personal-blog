from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer
from .services import user_create


class UserCreateApi(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_instance = user_create(**serializer.validated_data)

        return Response(
            {"detail": f"User {user_instance.username} has been created"},
            status=status.HTTP_201_CREATED,
        )
