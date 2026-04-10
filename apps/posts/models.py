import uuid_utils as uuid
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.utils import timezone


def generate_uuid7():
    return str(uuid.uuid7())


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        ARCHIVED = "AR", "Archived"

    id = models.UUIDField(primary_key=True, default=generate_uuid7, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="posts",
    )
    title = models.CharField(max_length=250)
    content = models.TextField(help_text="Write your blog post using Markdown")
    content_html = models.TextField(editable=False, blank=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    slug = models.SlugField(
        max_length=250, unique=True, db_index=True, allow_unicode=False
    )
    search_vector = models.GeneratedField(
        expression=SearchVector("title", config="english")
        + SearchVector("content", config="english"),
        output_field=SearchVectorField(),
        db_persist=True,
    )
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"], name="search_vector_idx"),
            models.Index(
                fields=["status", "deleted_at", "created_at"],
                name="status_deleted_created_idx",
            ),
        ]
