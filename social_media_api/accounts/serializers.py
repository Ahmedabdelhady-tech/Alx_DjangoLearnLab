from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from.models import CustomUser


User = get_user_model()  
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()    
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password','bio', 'profile_picture']
        


    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio = validated_data.get('bio', ''),
            profile_picture = validated_data.get('profile_picture', None)
        )
        
        Token.objects.create(user=user) 
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']