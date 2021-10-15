from rest_framework.views import APIView
from rest_framework import status
from .models import Notification
from accounts.models import Account
from .serializers import NotificationSerializer
from rest_framework.response import Response


class CreateNotification(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            username = data['username']
            type = data['type']
            by_user = Account.objects.get(username=self.request.user.username)
            to_user = Account.objects.get(username=username)
            if type == 'collaborate':
                text_one = str(by_user.username)
                highlighted_text = 'want to collaborate'
                text_two = 'with you'
            elif type == 'selected':
                text_one = 'you are selected in'
                highlighted_text = str(by_user.username)
                text_two = 'project'
            elif type == 'bid':
                text_one = str(by_user.username)
                highlighted_text = 'has replied'
                text_two = 'to your bid'
            notification = Notification.objects.create(by_user=by_user, to_user=to_user, type=type, text_one=text_one, highlighted_text=highlighted_text, text_two=text_two)
            serializer = NotificationSerializer(notification)
            return Response({'success': 'Successfully created notification', 'notification': serializer.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Something went wrong while creating notification'})


class SeenByUser(APIView):

    def put(self, request, format=None):
        try:
            user = Account.objects.get(username=self.request.user.username)
            Notification.objects.filter(to_user=user, seen_by_user=False).update(seen_by_user=True)
            return Response({'success': 'Successfully set seen notification'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while  setting seen  notification'})


class GetSeenNotifications(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            notifications = Notification.objects.filter(to_user=user, seen_by_user=True)
            serializers = NotificationSerializer(notifications, many=True)
            return Response({'success': 'Successfully fetched notifications', 'notifications': serializers.data})
        except:
            return Response({'error': 'Something went wrong while fetching unseen notifications'})


class GetUnSeenNotifications(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            notifications = Notification.objects.filter(to_user=user, seen_by_user=False)
            serializers = NotificationSerializer(notifications, many=True)
            return Response({'success': 'Successfully fetched notifications', 'notifications': serializers.data})
        except:
            return Response({'error': 'Something went wrong while fetching unseen notifications'})
