from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'avatar',
            'birthday',
            'age',
            'gender',
        )

        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True}
        }

    def create(self, validated_data):
        instance = self.Meta.model.objects.create_user(
            email=validated_data.pop('email'),
            first_name=validated_data.pop('first_name'),
            password=validated_data.pop('password', None),
            **validated_data
        )

        return instance
