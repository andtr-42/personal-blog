from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import post_create 
from .serializers import PostCreateSerializer

class PostCreateApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_instance = post_create(
            author = request.author,
            **serializer.validated_data
        )

        return Response({"id": post_instance.id}, status=status.HTTP_201_CREATED)
