from rest_framework import serializers
from .models import Resorts, Location, Adventures, Destinations
from account.models import User
from account.serializers import UserSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ResortSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    location = LocationSerializer()
    class Meta:
        model = Resorts
        fields = '__all__'

class PostResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resorts
        fields = '__all__'

class AdventureSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    resort = ResortSerializer()

    class Meta:
        model = Adventures
        fields = '__all__'

class PostAdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventures
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    resort = ResortSerializer()
    class Meta:
        model = Destinations
        fields = '__all__'

class PostDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'














        # owner = serializers.IntegerField(read_only=True,source='owner.id')