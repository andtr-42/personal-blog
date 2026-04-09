from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import post_create 
from .selectors import post_list, post_detail
from uuid_utils import uuid7
from .serializers import PostCreateSerializer, PostListSerializer, PostDetailSerializer

class PostApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        try:
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response({"error": "Invalid input! Please enter a number."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = post_list(
                reader = request.user, 
                limit= limit,
                offset= offset
            )
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostListSerializer(data["results"], many=True)

        return Response({
            "count": data["count"], 
            "limit": limit, 
            "offset": offset, 
            "results": serializer.data} , 
            status=status.HTTP_200_OK)

    def post(self, request):

        serializer_class = PostCreateSerializer

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_instance = post_create(
            author = request.user,
            **serializer.validated_data
        )

        return Response({"id": post_instance.id}, status=status.HTTP_201_CREATED)

class PostDetailApi(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, post_id):

        serializer_class = PostDetailSerializer

        data = post_detail(post_id)
    
        if not data:
            return Response({"error": f"Post with id of {post_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostDetailSerializer(data)

        return Response(serializer.data, status=status.HTTP_200_OK)

       
        






    

