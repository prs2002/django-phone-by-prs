from rest_framework import serializers
from .models import User, Contact
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'spam', 'spam_count', 'user']

class ContactSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    spam_count = serializers.IntegerField()
    is_spam = serializers.BooleanField()
    user_email = serializers.EmailField(allow_null=True)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(style={'input_type':'password'},max_length=25)

    class Meta:
        model = User
        fields = ('username','password')

    def validate(self, **kwargs):
       # some validation ( null check)
        def create(self, validated_data):
            username = self.validated_data.get("username", None)
            password = self.validated_data.get("password", None)
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is None:
                raise serializers.ValidationError('User Not Found')
            return user
