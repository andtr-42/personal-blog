from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    is_reader = serializers.BooleanField()
    is_writer = serializers.BooleanField()
