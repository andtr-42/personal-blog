from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .selectors import post_detail, post_list
from .serializers import PostCreateSerializer, PostDetailSerializer, PostListSerializer
from .services import post_create, post_update


class PostApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response(
                {"error": "Invalid input! Please enter a number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data = post_list(reader=request.user, limit=limit, offset=offset)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostListSerializer(data["results"], many=True)

        return Response(
            {
                "count": data["count"],
                "limit": limit,
                "offset": offset,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer_class = PostCreateSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_instance = post_create(author=request.user, **serializer.validated_data)

        return Response({"id": post_instance.id}, status=status.HTTP_201_CREATED)


class PostDetailUpdatelApi(APIView):
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return PostCreateSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request, post_id):
        data = post_detail(post_id)

        if not data:
            return Response(
                {"error": f"Post with id of {post_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            post_instance = post_update(
                post_id=post_id, author=request.user, **serializer.validated_data
            )

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response({"id": post_instance.id}, status=status.HTTP_200_OK)
