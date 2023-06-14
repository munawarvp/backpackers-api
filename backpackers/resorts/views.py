from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter
from .serializers import (LocationSerializer, ResortSerializer,PostResortSerializer, AdventureSerializer,PostAdventureSerializer
,DestinationSerializer, PostDestinationSerializer)
from .models import Location, Resorts, Adventures, Destinations
from booking.models import ResortBooking, AdventureBooking
from account.models import User
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# ***views for staff admin***

class LocationList(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ResortList(ListCreateAPIView):
    serializer_class = ResortSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        # print(user_id)
        queryset = Resorts.objects.filter(owner=user_id)
        return queryset
    
class CreateResort(APIView):
    def post(self, request, format=None):
        serializer = PostResortSerializer(data=request.data)
        print(request.data)
        is_valid = serializer.is_valid()
        print(serializer.errors)

        if serializer.is_valid():
            serializer.save()
            print('at last hope')
            return Response({'msg': 200})
        else :
            print('still no hope')
            return Response({'msg': 404})
        
    def get(self, request, resort_id=None):
        if resort_id is not None:
            queryset = Resorts.objects.get(id=resort_id)
            serializer = ResortSerializer(queryset)
            return Response(serializer.data)
        return Response({'msg': 404})
        
    def put(self, request, resort_id):
        try:
            queryset = Resorts.objects.get(id=resort_id)
        except:
            Resorts.DoesNotExist
            return Response({'msg': 404})
        # print(request.data)
        user_id = request.data['owner']
        location_id = request.data['location']
        user = User.objects.get(id=user_id)
        location = Location.objects.get(id=location_id) 
        
        data = request.data.copy()
        print(data)
        # data['owner'] = user
        # data['location'] = location

        
        serializer = PostResortSerializer(queryset, data=request.data)
        err = serializer.is_valid()
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200})
        else:
            return Response({'msg': 500})
        
    def delete(self, request, resort_id):
        try:
            queryset = Resorts.objects.get(id=resort_id)
            queryset.delete()
            return Response({'msg': 200})
        except:
            Resorts.DoesNotExist
            return Response({'msg': 500})

    
class SearchResorts(ListCreateAPIView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Resorts.objects.filter(owner=user_id)
        return queryset
    serializer_class = ResortSerializer
    filter_backends = [SearchFilter]
    queryset = Resorts.objects.all()
    search_fields = ['resort_name', 'place']

class AdminSearchResort(ListCreateAPIView):
    serializer_class = ResortSerializer
    filter_backends = [SearchFilter]
    queryset = Resorts.objects.all()
    search_fields = ['resort_name', 'place']

# use this view for both creating resort and listing resort in super admin panel
class ListResorts(viewsets.ModelViewSet):
    queryset = Resorts.objects.all()
    serializer_class = ResortSerializer

    def create(self, request, *args, **kwargs):
        serializer = ResortSerializer(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        # print(serializer.error_messages)
        if serializer.is_valid():
            serializer.save()
        # print the data that was passed in the request
            print('created')
            return Response(serializer.data)
        else:
            return Response({'msg': 404})
        

class StaffPendingResort(APIView):
    def get(self, request, id):
        queryset = Resorts.objects.filter(owner=id).filter(is_approved=False)
        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)

class FilterResorts(APIView):
    def get(self, request, id, value):
        if value == 1:
            queryset = Resorts.objects.filter(owner=id).filter(is_approved=True)
        elif value == 2:
            queryset = Resorts.objects.filter(owner=id).filter(is_approved=False)
        else:
            queryset = Resorts.objects.filter(owner=id).all()

        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)
    
class DashboardCount(APIView):
    def get(self, request):
        resort_count = Resorts.objects.count()
        resort_booking = ResortBooking.objects.count()
        adventure_booking = AdventureBooking.objects.count()
        total_booking = resort_booking + adventure_booking
        return Response({'resort_count':resort_count,'total_booking': total_booking})

    
class FilterActivity(APIView):
    def get(self, request, id, value):
        if value == 1:
            queryset = Adventures.objects.filter(owner=id).filter(is_approved=True)
        elif value == 2:
            queryset = Adventures.objects.filter(owner=id).filter(is_approved=False)
        else:
            queryset = Adventures.objects.filter(owner=id).all()

        serializer = AdventureSerializer(queryset, many=True)
        return Response(serializer.data)
    
class FilterDestination(APIView):
    def get(self, request, id, value):
        if value == 1:
            queryset = Destinations.objects.filter(owner=id).filter(is_approved=True)
        elif value == 2:
            queryset = Destinations.objects.filter(owner=id).filter(is_approved=False)
        else:
            queryset = Destinations.objects.filter(owner=id).all()

        serializer = DestinationSerializer(queryset, many=True)
        return Response(serializer.data)

# user side views starts    

class HomeListResorts(APIView):
    def get(self, request):
        queryset = Resorts.objects.filter(is_approved=True)[:4]
        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)
    
class HomeListAdventures(APIView):
    def get(self, request):
        queryset = Adventures.objects.filter(is_approved=True)[:4]
        serializer = AdventureSerializer(queryset, many=True)
        return Response(serializer.data)
    
class HomeListDestinations(APIView):
    def get(self, request):
        queryset = Destinations.objects.filter(is_approved=True)[:4]
        serializer = DestinationSerializer(queryset, many=True)
        return Response(serializer.data)

#pagination for user resort listing 
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 3

class UserResortList(ListCreateAPIView):
    queryset = Resorts.objects.filter(is_approved=True)
    serializer_class = ResortSerializer
    pagination_class = StandardResultsSetPagination
    # def get(self, request):
    #     queryset = Resorts.objects.filter(is_approved=True)
    #     page = self.pagination_class().paginate_queryset(queryset, request)
    #     next = self.page.paginator.count
    #     print(next)
        
    #     serializer = ResortSerializer(page, many=True)
    #     return Response(serializer.data)
    
class UserAdventureList(APIView):
    def get(self, request):
        queryset = Adventures.objects.filter(is_approved=True)
        serializer = AdventureSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserDestinationList(APIView):
    def get(self, request):
        queryset = Destinations.objects.filter(is_approved=True)
        serializer = DestinationSerializer(queryset, many=True)
        return Response(serializer.data)
    
class SingleResortView(APIView):
    def get(self, request, resort_id):
        queryset = Resorts.objects.get(id=resort_id)
        serializer = ResortSerializer(queryset)
        
        return Response(serializer.data)  
    
class SimilarStays(APIView):
    def get(self, request, resort_id):
        print(resort_id)
        queryset = Resorts.objects.all().exclude(id=resort_id)[:3]
        serializer = ResortSerializer(queryset, many=True)
        
        return Response(serializer.data) 
    
# user side views

# ****adventure view****
class StaffAdventureList(APIView):
    def post(self, request):
        serializer = PostAdventureSerializer(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200})
        return Response({'msg': 404})
    
    def get(self, request, user_id=None):
        if user_id is not None:
            queryset = Adventures.objects.filter(owner=user_id)
            serializer = AdventureSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = Adventures.objects.all()
            serializer = AdventureSerializer(queryset, many=True)
            return Response(serializer.data)
    
    def put(self, request, user_id):
        try:
            queryset = Adventures.objects.get(id=user_id)
        except:
            Adventures.DoesNotExist
            return Response({'msg': 'Product doesnot exist'})
        
        serializer = PostAdventureSerializer(queryset, data=request.data)
        serializer.is_valid()
        print(request.data)
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            print('saved')
            return Response(serializer.data)
        print('didnt saved')
        return Response({'msg': 404})
    
    def delete(self, request, user_id):
        try:
            queryset = Adventures.objects.get(id=user_id)
            queryset.delete()
            return Response({'msg': 200})
        except:
            Adventures.DoesNotExist
            return Response({'msg': 404})

class GetAdventureDetail(APIView):
    def get(self, request, act_id=None):
        if act_id is not None:
            queryset = Adventures.objects.get(id=act_id)
            serializer = AdventureSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({'msg':'get has nothing '})
        
class SearchAdventure(ListCreateAPIView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Adventures.objects.filter(owner=user_id)
        return queryset
    
    queryset = Adventures.objects.all()
    serializer_class = AdventureSerializer
    filter_backends = [SearchFilter]
    search_fields = ['activity_name', 'place']

class AdminSearchAdventure(ListCreateAPIView):
    queryset = Adventures.objects.all()
    serializer_class = AdventureSerializer
    filter_backends = [SearchFilter]
    search_fields = ['activity_name', 'place']
# ****adventure view****


# *** destination views ***
class StaffDashboardResort(APIView):
    def get(self, request, user_id):
        queryset = Resorts.objects.filter(owner=user_id)[:3]
        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)


class StaffDestinationList(APIView):
    def post(self, request):
        serializer = PostDestinationSerializer(data=request.data)
        err =serializer.is_valid()
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200})
        else:
            return Response({'msg': 504})
        
    def get(self, request, user_id=None):
        if user_id is not None:
            queryset = Destinations.objects.filter(owner=user_id)
            serializer = DestinationSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = Destinations.objects.all()
            serializer = DestinationSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def put(self, request, user_id):
        try:
            queryset = Destinations.objects.get(id=user_id)
        except:
            Destinations.DoesNotExist
            return Response({'msg': 404})
        serializer = PostDestinationSerializer(queryset, data=request.data)
        serializer.is_valid()
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 200})
        return Response({'msg': 500})

    def delete(self, request, user_id):
        try:
            queryset = Destinations.objects.get(id=user_id)
            queryset.delete()
            return Response({'msg': 200})
        except:
            return Response({'msg': 404})

class GetDestinationDeatail(APIView):
    def get(self, request, id=None):
        if id is not None:
            queryset = Destinations.objects.get(id=id)
            serializer = DestinationSerializer(queryset)
        else :
            queryset = Destinations.objects.all()
            serializer = DestinationSerializer(queryset, many=True)

        return Response(serializer.data)
    
class SearchDestinations(ListCreateAPIView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Destinations.objects.filter(owner=user_id)
        return queryset
    
    serializer_class = DestinationSerializer
    queryset = Destinations.objects.all()
    filter_backend = [SearchFilter]
    search_fields = ['spot_name', 'place']

class AdminSearchDestination(ListCreateAPIView):
    serializer_class = DestinationSerializer
    queryset = Destinations.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['spot_name', 'place']

# *** destination views ***

# ***views for staff admin***



# ***views for super admin***

class ListPendingResort(APIView):
    def get(self, request):
        queryset = Resorts.objects.filter(is_approved=False)
        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)

class SinglePendingResort(APIView):
    def get(self, request, pk):
        queryset = Resorts.objects.get(id=pk)
        serializer = ResortSerializer(queryset)
        return Response(serializer.data)
    
class ApproveResort(APIView):
    def get(self, request, user_id, pk):
        try:
            user = User.objects.get(id=user_id)
            resort = Resorts.objects.get(id=pk)
        except:
            raise NameError
        
        if (not user.is_staff):
            user.is_staff = True
            user.save()
            
            if (resort.is_rejected):
                resort.is_rejected = False
                resort.save()
            resort.is_approved = True
            resort.save()

            to_email = user.email
            resortname = resort.resort_name

            mail_subject = 'Congratulations..! Your resort got approval from our side.'
            message = render_to_string( 'accounts/resort_approval_email.html', {
                'user': user,
                'resort': resortname
            })
            
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg': 'user and resort updated'})
        else:
            if (resort.is_rejected):
                resort.is_rejected = False
                resort.save()
            resort.is_approved = True
            resort.save()
            return Response({'msg': 'resort only updated'})
        
class RejectResort(APIView):
    def delete(self, request, id):
        resort = Resorts.objects.get(id=id)
        resort.is_rejected = True
        resort.save()
        return Response({'msg': 200})
        
class BlockResort(APIView):
    def get(self, request, pk):
        resort = Resorts.objects.get(id=pk)
        resort.is_approved = not resort.is_approved
        resort.save()
        return Response({'msg': resort.is_approved})
    
class BlockAdventure(APIView):
    def get(self, request, pk):
        adventure = Adventures.objects.get(id=pk)
        adventure.is_approved = not adventure.is_approved
        adventure.save()
        return Response({'msg': adventure.is_approved})
    
class BlockDestination(APIView):
    def get(self, request, pk):
        destination = Destinations.objects.get(id=pk)
        destination.is_approved = not destination.is_approved
        destination.save()
        return Response({'msg': destination.is_approved})


class AdminFilterResorts(APIView):
    def get(self, request, value):
        if value == 1:
            queryset = Resorts.objects.filter(is_approved=True)
        elif value == 2:
            queryset = Resorts.objects.filter(is_approved=False)
        else:
            queryset = Resorts.objects.all()

        serializer = ResortSerializer(queryset, many=True)
        return Response(serializer.data)
    
class AdminFilterActivity(APIView):
    def get(self, request, value):
        if value == 1:
            queryset = Adventures.objects.filter(is_approved=True)
        elif value == 2:
            queryset = Adventures.objects.filter(is_approved=False)
        else:
            queryset = Adventures.objects.all()

        serializer = AdventureSerializer(queryset, many=True)
        return Response(serializer.data)
    
class AdminFilterDestination(APIView):
    def get(self, request, value):
        if value == 1:
            queryset = Destinations.objects.filter(is_approved=True)
        elif value == 2:
            queryset = Destinations.objects.filter(is_approved=False)
        else:
            queryset = Destinations.objects.all()

        serializer = DestinationSerializer(queryset, many=True)
        return Response(serializer.data)

