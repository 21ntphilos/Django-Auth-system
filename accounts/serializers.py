from rest_framework import serializers
from django.core.mail import send_mail

from django.contrib.auth import get_user_model

User = get_user_model()
class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'password': {'required': True}
        }

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                password=validated_data['password']
            )

            send_mail(
                subject='Welcome to Our APP',
                message=f'Hi {validated_data["full_name"]}, thank you for registering at our platform.',
                from_email='zerosandone01@gmail.com',
                fail_silently=False,
                recipient_list=[validated_data['email']],
            )
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        return user

