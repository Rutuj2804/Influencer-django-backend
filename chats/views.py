from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from .models import Message, ChatRoom
from .serializers import ChatRoomSerializer, MessageSerializer
from django.utils import timezone


class CreateChatRoom(APIView):

    def post(self, request, format=None):
        try:
            username = self.request.data['username']
            user = Account.objects.get(username=username)
            me = Account.objects.get(username=self.request.user.username)
            rooms = ChatRoom.objects.filter(users=me)
            for room in rooms:
                if room.users.filter(username=username).exists():
                    serializer = ChatRoomSerializer(room)
                    return Response({'success': 'Successfully fetched room', 'room': serializer.data})
            room = ChatRoom.objects.create()
            room.users.add(user)
            room.users.add(me)
            serializer = ChatRoomSerializer(room)
            return Response({'success': 'Successfully create room', 'room': serializer.data})
        except:
            return Response({'error': 'Something went wrong while creating a room'}, status=status.HTTP_400_BAD_REQUEST)


class GetChatRooms(APIView):

    def get(self, request, format=None):
        try:
            user = Account.objects.get(username=self.request.user.username)
            room = ChatRoom.objects.filter(users=user).order_by('-last_conversaion')
            serializer = ChatRoomSerializer(room, many=True)
            return Response({'success': 'Successfully fetched rooms', 'room': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching rooms'}, status=status.HTTP_400_BAD_REQUEST)


class AddMessages(APIView):

    def post(self, request, format=None):
        try:
            me = Account.objects.get(username=self.request.user.username)
            room_id = self.request.data['room_id']
            if ChatRoom.objects.filter(id=room_id).exists():
                message = Message.objects.create(text=self.request.data['message'], user=me)
                chat_room = ChatRoom.objects.get(id=room_id)
                ChatRoom.objects.filter(id=room_id).update(last_conversaion=timezone.now(), last_message=self.request.data['message'])
                chat_room.chats.add(message)
                serializer = MessageSerializer(message)
                return Response({'success': 'Successfully send message', 'message': serializer.data})
            else:
                return Response({'error':'No room mentioned while messaging'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while creating a room'}, status=status.HTTP_400_BAD_REQUEST)


class GetMessages(APIView):

    def post(self, request, format=None):
        try:
            id = self.request.data['id']
            if not ChatRoom.objects.filter(id=id).exists():
                return Response({'error': 'No such chat room exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                chat_room = ChatRoom.objects.get(id=id)
                messages = chat_room.chats.all().order_by('created_at')
                user = chat_room.users.all()
                if user[0].username == self.request.user.username:
                    user = user[1]
                else:
                    user = user[0]
                serializer = MessageSerializer(messages, many=True)
                user = AccountSerializer(user)
                return Response({'success': 'Successfully fetched messages', 'messages': serializer.data, 'user': user.data}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while fetching messages'}, status=status.HTTP_400_BAD_REQUEST)


class SeenMessages(APIView):

    def put(self, request, format=None):
        try:
            id = self.request.data['id']
            if not ChatRoom.objects.filter(id=id).exists():
                return Response({'error': 'No such chat room exists'}, status=status.HTTP_400_BAD_REQUEST)
            elif not ChatRoom.objects.get(id=id).chats.filter(user=self.request.user).exists():
                return Response({'error':'You are not allowed on this url'})
            else:
                chat_room = ChatRoom.objects.get(id=id)
                chat_room.chats.filter(seen_by_user=False).update(seen_by_user=True)
                return Response({'success': 'Successfully updated messages'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while fetching messages'}, status=status.HTTP_400_BAD_REQUEST)