from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}
    
    def check_password(self, raw_password):
        pattern = r"^\S{8,}$"
        if not re.match(pattern, raw_password):
            return False
        
        return True
     
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        
        user_exists = User.objects.filter(email=validated_data['email']).exists()
        
        if user_exists:
            raise ValidationError(detail={'email': 'Email already exists!'})
        
        if password is not None:
            user = self.Meta.model(**validated_data)
            
            if password != confirm_password:
                raise ValidationError(detail={'comfirm_password': 'Passwords do not match!'})
        
            if not self.check_password(password):
                raise serializers.ValidationError(
                    detail={'check_password': 'Password does not meet the requirements!\nPassword must be at least 8 characters long!\nPassword must not contain any spaces!'})
            
            user.set_password(password)
            user.confirm_password = user.password
            user.save()
            return user