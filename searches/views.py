from rest_framework.views import APIView
from rest_framework import status
from .models import Search
from accounts.models import Account
from accounts.serializers import AccountSerializer
from listings.models import Project
from listings.serializers import ProjectSerializer
from .serializers import SearchSerializer
from rest_framework.response import Response


class SetSearch(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            text = data['text']
            type = data['type']
            user = Account.objects.get(username=self.request.user.username)
            # Save search
            Search.objects.create(search_text=text, search_type=type, user=user)
            listings = Project.objects.filter(description__icontains=text) | Project.objects.filter(title__icontains=text)
            listing_serializer = ProjectSerializer(listings, many=True)
            users = Account.objects.filter(first_name__icontains=text) | Account.objects.filter(last_name__icontains=text) | Account.objects.filter(username__icontains=text)
            user_serializer = AccountSerializer(users, many=True)
            return Response({'success': 'Successfully fetched response', 'users': user_serializer.data, 'listings': listing_serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching response'})