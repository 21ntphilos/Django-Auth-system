from rest_framework import serializers

from django.contrib.auth import get_user_model

class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'full_name', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'password': {'required': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
       
        return user
    
