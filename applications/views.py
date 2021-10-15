from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Application
from accounts.models import Account
from accounts.serializers import AccountSerializer, SkillSerializer
from .serializers import ApplicationSerializer
from listings.serializers import RewardSerializer, WrokDescSerializer
from notifications.models import Notification
from chats.models import ChatRoom
from listings.models import Project
from listings.serializers import ProjectShortSerializer, ProjectSerializer


class GetMyApplicationAPIView(APIView):

    def get(self, request, format=None):
        try:
            user = Account.objects.get(username=self.request.user.username)
            project_list = Project.objects.all().order_by('-created_at')
            serializer_list = []
            for project in project_list:
                if project.applications.filter(applicant=user).exists():
                    user_serializer = AccountSerializer(project.user)
                    skill_serializer = SkillSerializer(project.requirements, many=True)
                    application_id = project.applications.filter(applicant=self.request.user)[0].id
                    application = Application.objects.get(id=application_id)
                    serializer = {
                        "id": project.id,
                        "title": project.title,
                        "description": project.description,
                        "type": project.type,
                        "created_at": project.created_at,
                        "place": project.place,
                        "payment": project.payment,
                        "target": project.target,
                        "completed": project.completed,
                        "deleted": project.deleted,
                        "positions": project.positions,
                        "requirements": skill_serializer.data,
                        "user": user_serializer.data,
                        "applications": project.applications.all().count(),
                        "status": application.status,
                        "applied_on": application.created_at
                    }
                    serializer_list.append(serializer)
            return Response({'success': 'Successfully fetched applications', 'applications': serializer_list}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while fetching applications'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateApplicationAPIView(APIView):

    def put(self, request, format=None):
        try:
            user = Account.objects.get(username=self.request.user.username)
            id = self.request.data['id']
            application_id = self.request.data['application_id']
            update = self.request.data['update']
            project = Project.objects.get(id=id)
            application = Application.objects.get(id=application_id)
            if project.user.username == user.username and project.applications.filter(applicant=application.applicant):
                if application.status != 'hired' and update == 'hired':
                    application.status = update
                    application.applicant.points = application.applicant.points + 10
                    application.applicant.save()
                    # notification
                    text_one = str(user.username) + ' has '
                    highlighted_text = 'accepted'
                    text_two=' your application'

                    rooms = ChatRoom.objects.filter(users=user)
                    chat_room = 0
                    for room in rooms:
                        if room.users.filter(username=application.applicant.username).exists():
                            chat_room = room
                            print('got chat room')
                            break
                    if not chat_room:
                        room = ChatRoom.objects.create()
                        room.users.add(application.applicant)
                        room.users.add(user)
                        print('new chat room')
                        chat_room = room
                    Notification.objects.create(by_user=user, to_user=application.applicant, type="project", text_one=text_one, highlighted_text=highlighted_text, text_two=text_two)
                    application.applicant.save()
                    application.save()
                    user_serializer = AccountSerializer(project.user)
                    applications_user_serializer = ApplicationSerializer(project.applications, many=True)
                    applications_views_serializer = AccountSerializer(project.views, many=True)
                    skill_serializer = SkillSerializer(project.requirements, many=True)
                    rewards_serializer = RewardSerializer(project.reward, many=True)
                    work_serializer = WrokDescSerializer(project.work_description, many=True)
                    serializer = {
                        "id": project.id,
                        "title": project.title,
                        "description": project.description,
                        "type": project.type,
                        "created_at": project.created_at,
                        "place": project.place,
                        "payment": project.payment,
                        "target": project.target,
                        "completed": project.completed,
                        "deleted": project.deleted,
                        "positions": project.positions,
                        "user": user_serializer.data,
                        "applications": applications_user_serializer.data,
                        "views": applications_views_serializer.data,
                        "requirements": skill_serializer.data,
                        "reward": rewards_serializer.data,
                        "work_description": work_serializer.data,
                        "room": chat_room.id
                    }
                    return Response({'success':'Successfully hired', 'project': serializer})
                elif application.status == 'hired' and update !='hired':
                    application.status = update
                    application.applicant.points = application.applicant.points - 10
                    application.applicant.save()
                else:
                    application.status = update
                application.save()
                serializer = ProjectSerializer(project)
                return Response({'success': 'Successfully updated applications', 'project': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You are not authorized to this url'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while fetching applications'}, status=status.HTTP_400_BAD_REQUEST)


