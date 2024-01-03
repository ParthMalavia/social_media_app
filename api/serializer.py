from rest_framework_simplejwt.tokens import Token
from .models import User, Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        
        token["full_name"] = user.profile.full_name
        token["username"] = user.username
        token["email"] = user.email
        token["bio"] = user.profile.bio
        token["image"] = str(user.profile.image)
        token["verified"] = user.profile.verified
        
        return token


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Add password validation
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password = serializers.CharField(write_only=True, required=True, validators=[])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]

    def validate(self, attr):
        if attr["password"] != attr["password2"]:
            raise serializers.ValidationError({"password" : "password field does not match"})
        return attr
    
    def create(self, attr):
        user = User.objects.create(
            username = attr['username'],
            email = attr['email'],
        )
        user.set_password(attr['password'])
        user.save()
        return user