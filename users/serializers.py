from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        
        if password is not None:
            user = self.Meta.model(**validated_data)
            if password != confirm_password:
                raise serializers.ValidationError({'warning': 'Passwords must match.'})
            user.set_password(password)
            user.confirm_password = user.password
            user.save()
            return user