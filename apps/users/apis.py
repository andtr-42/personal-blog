from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import user_create
from .serializers import UserCreateSerializer

class UserCreateApi(APIView):

    serializer_class = UserCreateSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_instance = user_create(
            **serializer.validated_data
        )

        return Response(status=status.HTTP_201_CREATED)
