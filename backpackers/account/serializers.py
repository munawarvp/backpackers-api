from rest_framework import serializers
from account.models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # #validate pass1 and pass2
    # def validate(self, data):
    #     password = data.get('password')
    #     password2 = data.get('confirm_pass')
    #     if password != password2:
    #         raise serializers.ValidationError("Passwords doesnot match")
    #     return data
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'