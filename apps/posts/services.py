import markdown
from django.db import transaction
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .models import Post
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

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

        post = Post.objects.create(author=author, title=title, content=content, content_html=content_html, status=status, slug=post_slug)

        return post 





  
