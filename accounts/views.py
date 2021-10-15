from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Skill, Link
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        try:
            data = self.request.data
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            email = data['email']
            password = data['password']
            city = data['city']
            state = data['state']
            if first_name != '' and username != '' and email != '' and city != '' and state != '':
                if not Account.objects.filter(username=username).exists():
                    user = Account.objects.create_user(first_name=first_name, email=email, username=username, password=password, city=city, state=state)
                    user.last_name = last_name
                    user.save()
                    token = Token.objects.create(user=user)
                    return Response({'token':token.key}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Every field is necessary'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while registering a user'}, status=status.HTTP_400_BAD_REQUEST)


class EditUserApiView(APIView):

    def put(self, request, format=None):
        try:
            data = self.request.data
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            email = data['email']
            city = data['city']
            state = data['state']
            desc = data['description']
            insta = data['instagram']
            facebook = data['facebook']
            youtube = data['youtube']
            skills = data['skills']
            links = data['links']
            if first_name != '' and last_name != '' and username != '' and email != '' and city != '' and state != '':
                if not Account.objects.filter(username=username).exists() or username==self.request.user.username:
                    user = Account.objects.filter(username=self.request.user.username).update(
                                                                                            first_name=first_name,
                                                                                            last_name=last_name,
                                                                                            username=username,
                                                                                            email=email,
                                                                                            city=city,
                                                                                            state=state,
                                                                                            description=desc,
                                                                                            instagram=insta,
                                                                                            facebook=facebook,
                                                                                            youtube=youtube
                                                                                        )
                    user = Account.objects.get(username=self.request.user.username)
                    for skill_existing in user.skills.all():
                        user.skills.remove(skill_existing)
                    for skill in skills:
                        if Skill.objects.filter(name=skill["name"].lower()).exists():
                            skill_instance = Skill.objects.get(name=skill['name'].lower())
                            user.skills.add(skill_instance)
                        else:
                            skill_instance = Skill.objects.create(name=skill['name'].lower())
                            user.skills.add(skill_instance)
                    for links_existing in user.links.all():
                        Link.objects.filter(id=links_existing.id)[0].delete()
                    for link in links:
                        link_instance = Link.objects.create(title=link['title'], link=link['link'])
                        user.links.add(link_instance)
                    user.save()
                    serializer = AccountSerializer(user)
                    return Response({'success':'Successfully edited user', 'user': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Every field is necessary'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while editing a user'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserApiView(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            user = Account.objects.get(username=user)
            serialzer = AccountSerializer(user)
            return Response(serialzer.data)
        except:
            return Response({'error': ''})


class CheckAuthentication(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            user = Account.objects.get(username=user)
            if user:
                return Response({'success': 'Is Authenticated'}, status=status.HTTP_200_OK)
            return Response({'error': 'Not Authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while checking authentication'}, status=status.HTTP_400_BAD_REQUEST)


class EditUserPhoto(APIView):

    def put(self, request, format=None):
        try:
            user = self.request.user
            user = Account.objects.get(username=user)
            user.photo = self.request.data['photo']
            user.save()
            serialzer = AccountSerializer(user)
            return Response({'success': 'Successfully updated photo','user':serialzer.data})
        except:
            return Response({'error': ''})


class StatusChangeOfUser(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data['status']
            print(data)
            user = Account.objects.get(username=self.request.user.username)
            if data == 'online':
                user.online = True
                user.save()
            elif data == 'offline':
                user.online = False
                user.save()
            return Response({'success': 'Successfully changed status'})
        except:
            return Response({'error': 'Something went wrong while changing status'})


class TopPerformers(APIView):

    def get(self, request, format=None):
        try:
            users = Account.objects.filter().order_by('-points')
            serializer = AccountSerializer(users[0:5], many=True)
            return Response({'success': 'Successfully fetched top rankers', 'rankers': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching rankers'})