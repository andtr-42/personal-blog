import markdown
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from .models import Post

CustomUser = get_user_model()


def post_create(*, author: CustomUser, title: str, content: str, status: str) -> Post:
    if not author.is_writer:
        raise ValidationError("User must be a writer to create a post.")

    # create the slug
    post_slug = slugify(title)

    temp_slug = post_slug

    # convert the Markdown content into HTML
    content_html = markdown.markdown(content)

    with transaction.atomic():
        # check if the slug is unique
        while Post.objects.filter(slug=temp_slug).exists():
            temp_slug = f"{post_slug}-{get_random_string(length=4)}"

        post_slug = temp_slug

        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
            content_html=content_html,
            status=status,
            slug=post_slug,
        )

        return post


def post_update(
    *,
    post_id: str,
    author: CustomUser,
    title: str = None,
    content: str = None,
    status: str = None,
) -> Post:
    if not author.is_writer:
        raise ValidationError("User must be a writer to update a post.")

    ps = Post.objects.select_related("author")

    post_instance = ps.filter(id=post_id, deleted_at=None).first()

    if not post_instance:
        raise Post.DoesNotExist

    if author.id != post_instance.author.id:
        raise PermissionError("Not valid author.")

    with transaction.atomic():
        updated_fields = []

        if title and post_instance.title != title:
            # create the slug
            post_slug = slugify(title)

            temp_slug = post_slug

            # check if the slug is unique
            while ps.filter(slug=temp_slug).exclude(id=post_instance.id).exists():
                temp_slug = f"{post_slug}-{get_random_string(length=4)}"

            post_slug = temp_slug

            post_instance.title = title
            post_instance.slug = post_slug

            updated_fields.append("title")
            updated_fields.append("slug")

        if content and post_instance.content != content:
            # convert the Markdown content into HTML
            content_html = markdown.markdown(content)

            post_instance.content = content
            post_instance.content_html = content_html

            updated_fields.append("content")
            updated_fields.append("content_html")

        if status and post_instance.status != status:
            post_instance.status = status
            updated_fields.append("status")

        if updated_fields:
            post_instance.updated_at = timezone.now()
            updated_fields.append("updated_at")

            post_instance.save(update_fields=updated_fields)

        return post_instance


def post_delete(*, post_id, author: CustomUser):
    if not author.is_writer:
        raise ValidationError("User must be a writer to update a post.")

    ps = Post.objects.select_related("author")

    post_instance = ps.filter(id=post_id, deleted_at=None).first()

    if not post_instance:
        raise Post.DoesNotExist

    if author.id != post_instance.author.id:
        raise PermissionError("Not valid author.")

    post_instance.deleted_at = timezone.now()

    post_instance.save()

    return post_instance
