from django.urls import path
from .apis import PostApi, PostDetailApi
from uuid_utils import uuid7

app_name = 'posts'
urlpatterns = [
    path('', PostApi.as_view(), name="list"),
    path('<str:post_id>', PostDetailApi.as_view(), name="detail"),

]