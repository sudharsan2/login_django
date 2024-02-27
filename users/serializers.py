from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user,userRoles,studentData, companyData, addUserExcel
from rest_framework.exceptions import AuthenticationFailed
class userRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = userRoles
        fields = "__all__"

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['username','email','roles']

class addUserExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = addUserExcel
        fields = ('excelFile')

class userRegistrationSerializer(serializers.ModelSerializer):
    # roles = userRoleSerializer()
    roles = serializers.CharField(max_length =20)
    # roles = serializers.PrimaryKeyRelatedField(queryset=userRoles.objects.all(), required=True)

    class Meta:
        model = user
        fields = ['username', 'email', 'password', 'roles']

    def create(self, validated_data):
        roles_data = validated_data.pop('roles')
        role_instance = userRoles.objects.get(role = roles_data)
        validated_data['roles'] = role_instance
        user_instance= user.objects.create_user(**validated_data)
    
        return user_instance
        
        
class loginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255)

    class Meta:
        model = user
        fields = ['username', 'password', 'tokens']
    
    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        return {
            'username': user.username,
            'tokens': user.tokens()
        }
    




            
        