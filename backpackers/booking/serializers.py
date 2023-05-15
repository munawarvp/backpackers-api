from .models import ResortBooking, AdventureBooking, ResortReviews, AdventureReviews, DestinationReviews, Coupon, CouponAssign, ResortPayments
from rest_framework import serializers

from account.serializers import UserSerializer
from resorts.serializers import ResortSerializer, AdventureSerializer, DestinationSerializer



class ResortBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    booked_resort = ResortSerializer()
    class Meta:
        model = ResortBooking
        fields = '__all__'

class PostResortBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResortBooking
        fields = '__all__'

                    
                    #\ ******************************************** /

class AdventureBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    booked_activity = AdventureSerializer()
    class Meta:
        model = AdventureBooking
        fields = '__all__'

class PostAdventureBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdventureBooking
        fields = '__all__'

                    
                     #\ ******************************************** /

class ResortReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    resort = ResortSerializer()
    class Meta:
        model = ResortReviews
        fields = '__all__'

class PostResortReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResortReviews
        fields = '__all__'

                   
                   #\ ******************************************** /

class AdventureReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    adventure = AdventureSerializer()
    class Meta:
        model = AdventureReviews
        fields = '__all__'

class PostAdventureReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdventureReviews
        fields = '__all__'


                   #\ ******************************************** /

class DestinationReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    destination = DestinationSerializer()
    class Meta:
        model = DestinationReviews
        fields = '__all__'


class PostDestinationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationReviews
        fields = '__all__'


                   #\ ******************************************** /


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponAssignSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer()
    class Meta:
        model = CouponAssign
        fields = '__all__'


                    #\ ******************************************** /


class ResortPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResortPayments
        fields = '__all__'