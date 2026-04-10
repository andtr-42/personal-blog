from rest_framework import serializers

from .models import Post


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=[("DF", "Draft"), ("PB", "Published")])


class PostListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    content_html = serializers.CharField()
    comment_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    author_username = serializers.CharField(source="author.username")
    is_published = serializers.SerializerMethodField()

    def get_is_published(self, obj):
        return obj.status == Post.Status.PUBLISHED


class PostDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    content_html = serializers.CharField()
    comment_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    author_username = serializers.CharField(source="author.username")
