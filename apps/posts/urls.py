from django.urls import path
from .apis import PostCreateApi

app_name = 'posts'
urlpatterns = [
    path('', PostCreateApi.as_view(), name="create")
]