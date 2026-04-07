from django.urls import path
from .apis import UserCreateApi

app_name= 'users'
urlpatterns = [
    path('', UserCreateApi.as_view(), name="create")
]