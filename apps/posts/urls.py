from django.urls import path
from .apis import PostApi

app_name = 'posts'
urlpatterns = [
    path('', PostApi.as_view(), name="list"),
]