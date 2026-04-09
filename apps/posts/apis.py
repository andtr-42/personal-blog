from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import post_create 
from .selectors import post_list
from .serializers import PostCreateSerializer, PostListSerializer

class PostApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCreateSerializer

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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_instance = post_create(
            author = request.user,
            **serializer.validated_data
        )

        return Response({"id": post_instance.id}, status=status.HTTP_201_CREATED)


    

