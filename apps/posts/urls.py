from django.urls import path

from .apis import PostApi, PostDetailUpdateDeleteApi

app_name = "posts"
urlpatterns = [
    path("", PostApi.as_view(), name="list"),
    path("<str:post_id>/", PostDetailUpdateDeleteApi.as_view(), name="detail_update"),
]
