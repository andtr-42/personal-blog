from rest_framework import serializers 

class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=[('DF', 'Draft'), ('PB', 'Published')])
    
