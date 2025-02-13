from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )

        return data

    def create(self, validated_data):
        validated_data.pop("password2") 

        user = User.objects.create_user(**validated_data)

        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return {
                'refresh': str(refresh),
                'access': access_token
            }
        raise serializers.ValidationError(
            {"오류": "일치하는 유저 정보가 없습니다."}
        )