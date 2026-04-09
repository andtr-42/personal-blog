from typing import Dict, Any
from django.db.models import QuerySet
from .models import Post
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

def post_list(*, reader: CustomUser, limit: int = 10, offset: int = 0) -> Dict[str, Any]:

    if not reader.is_reader:
        raise ValidationError("User must be a reader to read the posts.")

    qs = Post.objects.filter(status=Post.Status.PUBLISHED, deleted_at=None)

    qs = qs.select_related("author").order_by('-created_at', 'id')

    total_count = qs.count()

    return {
        "count": total_count,
        "results": qs[offset: offset + limit]
    }

def post_detail(post_id: str) -> Post:

    qs = Post.objects.select_related("author")

    qs = qs.filter(id=post_id, status=Post.Status.PUBLISHED, deleted_at=None).first()

    if not qs:
        return None

    return qs
