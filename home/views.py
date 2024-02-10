from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout,authenticate
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer, UserRegistrationSerializer, UserLoginSerializer

# @login_required(login_url='/login')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

# class SearchByPhoneNumber(APIView):
#     def get(self, request, format=None):
#         phone_number = request.query_params.get('phone_number', None)
#         if phone_number:
#             try:
#                 # Check if there's a registered user with the provided phone number
#                 user = User.objects.get(phone_number=phone_number)
#                 serializer = UserSerializer(user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 # If no registered user, search contacts table for matching phone number
#                 contacts = Contact.objects.filter(phone_number=phone_number)
#                 serializer = ContactSerializer(contacts, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Phone number parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

# class SearchByName(APIView):
#     def get(self, request, format=None):
#         name_query = request.query_params.get('name', None)
#         if name_query:

#             starts_with = Contact.objects.filter(name__istartswith=name_query)

#             contains = Contact.objects.filter(name__icontains=name_query).exclude(name__istartswith=name_query)

#             search_results = list(starts_with) + list(contains)
#             serializer = ContactSerializer(search_results, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Name parameter is required'}, status=status.HTTP_400_BAD_REQUEST) 

class Search(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query', None)
        if query:
            # Check if the query is a valid phone number
            if query.isdigit():
                try:
                    # Check if there's a registered user with the provided phone number
                    user = User.objects.get(phone_number=query)
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    contacts = Contact.objects.filter(phone_number=query)
                    serializer = ContactSerializer(contacts, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                contacts = Contact.objects.filter(name__icontains=query)
                serializer = ContactSerializer(contacts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'msg': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkUserAsSpam(APIView):
    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        if phone_number:
            try:
                contact = Contact.objects.get(phone_number=phone_number)
                contact.is_spam = True
                contact.spam_count += 1
                contact.save()
                return Response({'msg': 'User marked as spam successfully'}, status=status.HTTP_200_OK)
            except Contact.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Phone number not provided'}, status=status.HTTP_400_BAD_REQUEST)