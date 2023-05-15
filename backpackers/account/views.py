from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

from .serializers import UserSerializer, UserProfileSerializer
from account.models import User, UserProfile
from booking.models import Coupon, CouponAssign

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        '/token/refresh'
    ]
    return Response(routes)


class UserRegistration(APIView):
     def post(self, request, format=None):
          email = request.data.get('email')
          print(request.data)
          #storing userdata in session
          #request.session['userdata'] = request.data

          serializer = UserSerializer(data=request.data)
          #print(serializer.is_valid())
          if serializer.is_valid(raise_exception=True):
            
            user = serializer.save()
            
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            mail_subject = 'Please activate your account'
            
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'usename': urlsafe_base64_encode(force_bytes(user.username))
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg':'Registration Success'})
            

          return Response({'msg':'Registration Failed'})


@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        # userdata = request.session.get('userdata')
        # print('userd',userdata)
        # url = reverse('http://localhost:3000/login')

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()
        coupon = Coupon.objects.get(coupon_name='REGISTER')
        user_coupon = CouponAssign.objects.create(user=user, coupon=coupon)
        # user_coupon.save()
        print(user_coupon)
        print('saved')


        return HttpResponseRedirect('http://localhost:3000/login')
        # return Response({"msg": "activated"})
    

# customizing jwt token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_superadmin 

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ForgotPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if User.objects.filter(email=email).exists:
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg':'Please Reset Password In The Link', 'user_id':user.id})
        
        return Response({'msg': 'No Account Registered With This Email'})

@api_view(['GET'])    
def reset_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid

        sessionid = request.session.get('uid')
        print(sessionid)

        return HttpResponseRedirect('http://localhost:3000/reset-password/')
    
    return Response({'msg': 'Link Expired or Invalid Token'})
    


class ResetPassword(APIView):
    def post(self, request, format=None):
        # print(request.data)
        str_user_id = request.data.get('user_id')
        user_id = int(str_user_id)
        password = request.data.get('password')
        
        print(user_id)
        if user_id :
            # print(type(user_id))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            print('saved')

            return Response({'msg': 'Password Updated Successfully'})
    
        return HttpResponseRedirect('http://localhost:3000/reset-password')
    


# for listing the staffs only in super admin panel
class ListStaffs(APIView):
    def get(self, request):
        queryset = User.objects.filter(is_staff=True).exclude(is_superadmin=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
class AdminSearchStaff(ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    queryset = User.objects.filter(is_staff=True).exclude(is_superadmin=True)
    search_fields = ['username', 'email']  

class BlockStaff(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        print(user.is_active)
        user.is_active = not user.is_active
        user.save()
        return Response({'status':user.is_active})

class GetUserDetails(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user_id)
        print(user)
        serializer = UserSerializer(user)
        user_serializer = UserProfileSerializer(user_profile)
        response_data = {
            'user': serializer.data,
            'user_profile': user_serializer.data
        }
        return Response(response_data)
        
class CreateUserProfile(APIView):
    def put(self, request, user_id):
        print(request.data)
        # user_id = request.data['user']
        # print(request.data['profile_img'])
        user = UserProfile.objects.get(id=user_id)
        
        
        serializer = UserProfileSerializer(instance=user, data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            print('savedddd')
            serializer.save()
            return Response({'msg': 200})

        return Response({'msg': 500})