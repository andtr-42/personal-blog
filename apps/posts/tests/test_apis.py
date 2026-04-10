import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Post
from .factories import PostFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestPostDeleteAPI:
    def test_delete_post_success(self, api_client):
        user = UserFactory(is_writer=True)
        post = PostFactory(author=user)
        api_client.force_authenticate(user=user)

        url = reverse("posts:detail_update_delete", kwargs={"post_id": post.id})
        response = api_client.delete(url)

        if response.status_code == 400:
            print(f"\nDEBUG ERROR DATA: {response.data}")

        assert response.status_code == status.HTTP_200_OK

        post.refresh_from_db()
        assert post.deleted_at is not None

    def test_delete_post_unauthorized(self, api_client):
        user_a = UserFactory(is_writer=True)
        user_b = UserFactory(is_writer=True)

        post_b = PostFactory(author=user_b)
        api_client.force_authenticate(user=user_a)

        url = reverse("posts:detail_update_delete", kwargs={"post_id": post_b.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.filter(id=post_b.id).exists()  # Post still exists!
