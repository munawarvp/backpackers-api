from django.shortcuts import render
import datetime
import razorpay
import json
import datetime
from decouple import config
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .models import ResortBooking, AdventureBooking, ResortReviews, AdventureReviews, DestinationReviews, Coupon, CouponAssign, ResortPayments
from resorts.models import Resorts
from account.models import User
from .serializers import (PostResortBookingSerializer, ResortBookingSerializer, AdventureBookingSerializer, PostAdventureBookingSerializer,
                          PostResortReviewSerializer, PostAdventureReviewSerializer, ResortReviewSerializer, AdventureReviewSerializer,
                          PostDestinationReviewSerializer, DestinationReviewSerializer, CouponSerializer, CouponAssignSerializer, ResortPaymentSerializer)

# Create your views here.

class CheckResortAvailability(APIView):
    def get(self, request, date):
        sample = json.loads(date)
        check_in=sample['check_in']
        check_out=sample['check_out']
        checking_resort = sample['checking_resort']

        checkin_obj = datetime.datetime.fromisoformat(check_in)
        checkout_obj = datetime.datetime.fromisoformat(check_out)

        availability_case1 = ResortBooking.objects.filter(booked_resort=checking_resort, check_in__lte=checkin_obj, check_out__gte=checkin_obj).exists()
        availability_case2 = ResortBooking.objects.filter(booked_resort=checking_resort, check_in__lte=checkout_obj, check_out__gte=checkout_obj).exists()
        availability_case3 = ResortBooking.objects.filter(booked_resort=checking_resort, check_in__gte=checkin_obj, check_out__lte=checkout_obj).exists()

        print(availability_case1, availability_case2, availability_case3)

        if availability_case2 or availability_case1 or availability_case3:
            return Response({'msg': 504})
        else:
            return Response({'msg': 200})


class CreateResortBooking(APIView):
    def post(self, request):

        ch_in = request.data['check_in']
        ch_out = request.data['check_out']
        booking_total_str = request.data['booking_total']
        booking_total = int(booking_total_str)
        print(type(booking_total))
        resort_id = request.data['booked_resort']
        str_coupon_used = request.data['coupon_id']

        coupon_used = int(str_coupon_used)
        coupon_user = request.data['user']
        # if coupon_used == 0:
        #     print('no coupon')
        # else:
        #     print(coupon_used, 'used coupon')

        availability_case1 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__lte=ch_in, check_out__gte=ch_in).exists()
        availability_case2 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__lte=ch_out, check_out__gte=ch_out).exists()
        availability_case3 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__gte=ch_in, check_out__lte=ch_out).exists()
        print(availability_case1, 'case one')
        
        if availability_case2 or availability_case1 or availability_case3:
            return Response({'msg': 504})
        else:
            count = ResortBooking.objects.last()
            id = request.data['user']
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            if count is None:
                booking_id = current_date + str(id) + str(1)
            else:
                booking_id = current_date + str(id) + str(count.id+1)
            print(booking_id)
            data = request.data.copy()
            data['booking_id'] = booking_id
            print(data)
            
            serializer = PostResortBookingSerializer(data=data)
            serializer.is_valid()
            print(serializer.errors)
            if(serializer.is_valid()):
                if coupon_used == 0:
                    serializer.save()

                    if booking_total > 5000:
                        coupon = Coupon.objects.filter(is_active=True).exclude(coupon_name="REGISTER")
                        if coupon:
                            random_coupon = coupon.order_by('?').first()
                        got_user = User.objects.get(id=coupon_user)
                        user_coupon, created = CouponAssign.objects.get_or_create(user=got_user, coupon=random_coupon)
                        print(user_coupon, created)
                        if created:
                            coupon_serializer = CouponAssignSerializer(user_coupon)
                            return Response({'msg': 200, 'booking_id': booking_id, 'coupon_serializer': coupon_serializer.data})
                        
                    return Response({'msg': 200, 'booking_id': booking_id})
                else:
                    serializer.save()
                    used_coupon = CouponAssign.objects.get(coupon=coupon_used, user=coupon_user)
                    used_coupon.delete()
                    print('deleted')
                    return Response({'msg': 200, 'booking_id': booking_id})
            return Response({'msg': 404})
        

@api_view(['POST'])
def start_payment(request):
    amount = request.data['amount']
    form = json.loads(request.data["form"])
    print(form)

    ch_in = form['check_in']
    ch_out = form['check_out']
    resort_id = form['booked_resort']
    str_coupon_used = form['coupon_id']
    coupon_used = int(str_coupon_used)
    coupon_user = form['user']

    availability_case1 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__lte=ch_in, check_out__gte=ch_in).exists()
    availability_case2 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__lte=ch_out, check_out__gte=ch_out).exists()
    availability_case3 = ResortBooking.objects.filter(booked_resort=resort_id, check_in__gte=ch_in, check_out__lte=ch_out).exists()

    print(availability_case1, 'case one')
    print(availability_case2, 'case two')
    print(availability_case3, 'case three')

    if availability_case2 or availability_case1 or availability_case3:
        return Response({'msg': 504})
    else:
        client = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY')))

        payment = client.order.create({"amount": int(amount) * 100, 
                                    "currency": "INR", 
                                    "payment_capture": "1"})
    
    data = {
        "payment": payment
    }
    return Response(data)

@api_view(['POST'])
def activity_pay(request):
    amount = request.data['amount']
    form = json.loads(request.data["form"])

    client = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY')))
    payment = client.order.create({"amount": int(amount) * 100, 
                                    "currency": "INR", 
                                    "payment_capture": "1"})
    
    data = {
        "payment": payment
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    res = json.loads(request.data["response"])
    print(res['razorpay_payment_id'], 'ra_pay_id')
    form = json.loads(request.data["form"])

    coupon_user = form['user']
    paid_user = User.objects.get(id=coupon_user)

    str_coupon_used = form['coupon_id']
    coupon_used = int(str_coupon_used)
    print(res, 'res')
    booking_total_str = form['booking_total']
    booking_total = int(booking_total_str)

    count = ResortBooking.objects.last()
    id = form['user']
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    if count is None:
        booking_id = current_date + str(id) + str(1)
    else:
        booking_id = current_date + str(id) + str(count.id+1)
    
    form['booking_id'] = booking_id
    print(form, 'data')

    serializer = PostResortBookingSerializer(data=form)
    serializer.is_valid()
    print(serializer.errors)

    if(serializer.is_valid()):
        if coupon_used == 0:
            serializer.save()
            payment = ResortPayments.objects.create(user=paid_user,
                                                    order = booking_id,
                                                    payment_id = res['razorpay_payment_id'],
                                                    status = "Paid")
            
            print(payment,'created')

            if booking_total > 5000:
                coupon = Coupon.objects.get(coupon_name='EXPLORER')
                got_user = User.objects.get(id=coupon_user)
                user_coupon, created = CouponAssign.objects.get_or_create(user=got_user, coupon=coupon)
                print(user_coupon, created)
                if created:
                    coupon_serializer = CouponAssignSerializer(user_coupon)
                    return Response({'msg': 200, 'booking_id': booking_id, 'coupon_serializer': coupon_serializer.data})
                
            return Response({'msg': 200, 'booking_id': booking_id})
        
        else:
            serializer.save()
            used_coupon = CouponAssign.objects.get(coupon=coupon_used, user=coupon_user)
            used_coupon.delete()
            payment = ResortPayments.objects.create(user=paid_user,
                                                    order = booking_id,
                                                    payment_id = res['razorpay_payment_id'],
                                                    status = "Paid")
            print('deleted')
            return Response({'msg': 200, 'booking_id': booking_id})
    
    return Response({'msg': 504})


@api_view(['POST'])
def activity_payment_success(request):
    res = json.loads(request.data["response"])
    form = json.loads(request.data["form"])

    user = form['user']
    paid_user = User.objects.get(id=user)

    count = AdventureBooking.objects.last()
    id = form['user']
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    if count is None:
        booking_id = current_date + str(id) + str(1)
    else:
        booking_id = current_date + str(id) + str(count.id+1)

    form['booking_id'] = booking_id
    print(form, 'data')

    serializer = PostAdventureBookingSerializer(data=form)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 200, 'booking_id': booking_id})
    return Response({'msg': 504})

class CancelResortBooking(APIView):
    def get(self, request, booking_id):
        queryset = ResortBooking.objects.get(id=booking_id)
        queryset.status = "Cancelled"
        queryset.save()
        return Response({'msg': 200})

class AdminListBookings(APIView):
    def get(self, request):
        queryset = ResortBooking.objects.all().order_by('-booking_date')
        serializer = ResortBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GetBookingSummary(APIView):
    def get(self, request, booking_id):
        queryset = ResortBooking.objects.get(booking_id=booking_id)
        serializer = ResortBookingSerializer(queryset)
        return Response(serializer.data)

class GetResortPayment(APIView):
    def get(self, request, booking_id):
        try:
            queryset = ResortPayments.objects.get(order=booking_id)
        except:
            return Response({'msg': 404})
        serializer = ResortPaymentSerializer(queryset)
        return Response(serializer.data)
    
class RecentResortBookings(APIView):
    def get(self, request):
        queryset = ResortBooking.objects.all().order_by('-booking_date')[:4]
        serializer = ResortBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
class RecentActivityBookings(APIView):
    def get(self, request):
        queryset = AdventureBooking.objects.all().order_by('-booking_date')[:4]
        serializer = AdventureBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    

class StaffListBookings(APIView):
    def get(self, request, user_id):
        queryset = ResortBooking.objects.filter(booked_resort__owner = user_id).order_by('-booking_date')
        print(queryset)
        serializer = ResortBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ChangeResortBookingStatus(APIView):
    def get(self, request, value, booking_id):
        queryset = ResortBooking.objects.get(booking_id = booking_id)
        if value == 2:
            queryset.status = "Checked In"
            queryset.save()
            return Response({'msg': 200})
        elif value == 3:
            queryset.status = "Checked Out"
            queryset.save()
            return Response({'msg': 200})
        return Response({'msg': 404})
    
class StaffResortBookingFilter(APIView):
    def get(self, request, user_id, value):
        if value == 1:
            queryset = ResortBooking.objects.filter(booked_resort__owner=user_id, status="New")
        elif value == 2:
            queryset = ResortBooking.objects.filter(booked_resort__owner=user_id, status="Checked In")
        elif value == 3:
            queryset = ResortBooking.objects.filter(booked_resort__owner=user_id, status="Checked Out")
        elif value == 4:
            queryset = ResortBooking.objects.filter(booked_resort__owner=user_id, status="Cancelled")
        else: 
            queryset = ResortBooking.objects.filter(booked_resort__owner=user_id)

        serializer = ResortBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
class StaffSearchResortBooking(ListCreateAPIView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = ResortBooking.objects.filter(booked_resort__owner=user_id)
        return queryset
    queryset = ResortBooking.objects.all()
    serializer_class = ResortBookingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['booking_id']


# adventure bookings

class CreateAdventureBooking(APIView):
    def post(self, request):
        count = AdventureBooking.objects.last()
        if count:
            count = count.id
        else:
            count = 1
        id = request.data['user']
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        booking_id = current_date + str(id) + str(count+1)
        print(booking_id)
        data = request.data.copy()
        data['booking_id'] = booking_id
        print(data)
 
        serializer = PostAdventureBookingSerializer(data=data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200, 'booking_id': booking_id})
        return Response({'msg': 504})
   
    
class ListAdventureBookings(APIView):
    def get(self, request):
        queryset = AdventureBooking.objects.all().order_by('-booking_date')
        serializer = AdventureBookingSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAdventureBooking(APIView):
    def get(self, request, booking_id):
        queryset = AdventureBooking.objects.get(booking_id=booking_id)
        serializer = AdventureBookingSerializer(queryset)
        return Response(serializer.data)
    

class StaffAdventureBookings(APIView):
    def get(self, request, user_id):
        queryset = AdventureBooking.objects.filter(booked_activity__owner=user_id).order_by('-booking_date')
        serializer = AdventureBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    

class UserResortBookings(APIView):
    def get(self, request, user_id):
        queryset = ResortBooking.objects.filter(user=user_id)
        serializer = ResortBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserAdventureBookings(APIView):
    def get(self, request, user_id):
        queryset = AdventureBooking.objects.filter(user=user_id)
        serializer = AdventureBookingSerializer(queryset, many=True)
        return Response(serializer.data)

#\ ******************************************** /


class AddResortReview(APIView):
    def post(self, request):
        user = request.data['user']
        resort = request.data['resort']
        if user == '' :
            return Response({'msg': 501})
        else:
            queryset = ResortBooking.objects.filter(user__id=user, booked_resort=resort).exists()
            user_experienced = ResortBooking.objects.filter(user__id=user, booked_resort=resort, status__in=["Checked In", "Checked Out"]).exists()

            print(user, resort)
            print(queryset,'review query')

            review = ResortReviews.objects.filter(user=user, resort=resort).exists()
            
            print(user_experienced,'status check')

            if not user_experienced:
                return Response({'msg': 503})
            if review:
                return Response({'msg': 502})

            if queryset :
                serializer = PostResortReviewSerializer(data=request.data)
                serializer.is_valid()
                print(serializer.errors)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': 200})
                else:
                    return Response({'msg': 500})
            
            else:
                return Response({'msg': 404})
            
class AddAdventureReview(APIView):
    def post(self, request):
        user = request.data['user']
        adventure = request.data['adventure']
        if user == '' :
            return Response({'msg': 501})
        else:
            queryset = AdventureBooking.objects.filter(user__id=user, booked_activity=adventure).exists()

            if queryset:
                serializer = PostAdventureReviewSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': 200})
                else:
                    return Response({'msg': 500})
            else:
                return Response({'msg': 404})
            
class AddDestinationReview(APIView):
    def post(self, request):
        user = request.data['user']
        if user == '' :
            return Response({'msg': 501})
        else:
            # queryset = AdventureBooking.objects.filter(user__id=user, booked_activity=adventure).exists()
            # if queryset:
            serializer = PostDestinationReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 200})
            else:
                return Response({'msg': 500})
        # else:
        #     return Response({'msg': 404})

class ListResortReviews(APIView):
    def get(self, request, resort_id):
        print(resort_id)
        queryset = ResortReviews.objects.filter(resort__id=resort_id).order_by('-rating')[:3]
        print(queryset)
        serializer = ResortReviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ListAdventureReviews(APIView):
    def get(self, request, resort_id):
        queryset = AdventureReviews.objects.filter(adventure__id=resort_id).order_by('-rating')[:3]
        serializer = AdventureReviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ListDestinationReviews(APIView):
    def get(self, request, resort_id):
        queryset = DestinationReviews.objects.filter(destination__id=resort_id).order_by('-rating')[:3]
        serializer = DestinationReviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
class DeleteResortReview(APIView):
    def delete(self, request, review_id):
        try:
            queryset = ResortReviews.objects.get(id=review_id)
            queryset.delete()
            return Response({'msg': 200})
        except:
            return Response({'msg': 404})
        
class GetReviewImages(APIView):
    def get(self, request):
        resort_review = ResortReviews.objects.all().order_by('-rating')[:3]
        resort = ResortReviewSerializer(resort_review, many=True)

        adventure_review = AdventureReviews.objects.all().order_by('-rating')[:2]
        adventure = AdventureReviewSerializer(adventure_review, many=True)

        data = {
            'resort': resort.data,
            'adventure': adventure.data
        }
        return Response(data)


#\ ******************************************** /


class ListCoupons(APIView):
    def get(self, request):
        queryset = Coupon.objects.all()
        if queryset:
            random_coupon = queryset.order_by('?').first()
            print(random_coupon,'random')
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data)

class UserListCoupons(APIView):
    def get(self, request, user_id):
        queryset = CouponAssign.objects.filter(user=user_id)
        serializer = CouponAssignSerializer(queryset, many=True)
        return Response(serializer.data)

class AddCoupon(APIView):
    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200})
        return Response({'msg': 500})
    
class DeleteCoupon(APIView):
    def get(self, request, c_id):
        coupone = Coupon.objects.get(id=c_id)
        if coupone:
            coupone.delete()
            return Response({'msg': 200})
        return Response({'msg': 500})