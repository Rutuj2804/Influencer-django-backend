from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, WorkDescription, Reward
from accounts.models import Account, Skill
from accounts.serializers import AccountSerializer, SkillSerializer
from applications.models import Application
from .serializers import ProjectSerializer, WrokDescSerializer, RewardSerializer
from applications.serializers import ApplicationSerializer


class CreateListing(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            title = data['title']
            description = data['description']
            user = Account.objects.get(username=self.request.user.username)
            type = data['type']
            requirements = data['requirements']
            place = data['place']
            payment = data['money']
            work_description = data['work_description']
            reward = data['reward']
            target = data['target']
            position = data['position']
            if not title or not description:
                return Response({'error': 'Title and description are required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                project = Project.objects.create(title=title, description=description, user=user, type=type, place=place, payment=payment, target=target, positions=position)
                for work in work_description:
                    work = WorkDescription.objects.create(text=work['text'])
                    project.work_description.add(work)
                for reward_instance in reward:
                    reward_instance = Reward.objects.create(text=reward_instance['text'])
                    project.reward.add(reward_instance)
                for skill in requirements:
                    if Skill.objects.filter(name=skill["name"].lower()).exists():
                        skill_instance = Skill.objects.get(name=skill['name'].lower())
                        project.requirements.add(skill_instance)
                    else:
                        skill_instance = Skill.objects.create(name=skill['name'].lower())
                        project.requirements.add(skill_instance)
                project.save()
                user.points = user.points + 2
                user.save()
                serializer = ProjectSerializer(project)
                return Response({'success': 'Successfully created listing', 'listing': serializer.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Something went wrong while creating listing'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteListing(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            project = Project.objects.get(id=id)
            user = Account.objects.get(username=self.request.user.username)
            if project.user == user:
                project.deleted = True
                project.save()
                user.points = user.points - 10
                user.save()
                serializer = ProjectSerializer(project)
                return Response({'success': 'Successfully deleted listing', 'listing': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'You are not authorised to this url'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while creating listing'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateListing(APIView):

    def put(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            title = data['title']
            description = data['description']
            user = Account.objects.get(username=self.request.user.username)
            type = data['type']
            requirements = data['requirements']
            place = data['place']
            payment = data['payment']
            work_description = data['work_description']
            reward = data['reward']
            target = data['target']
            if not title or not description:
                return Response({'error': 'Title and description are required'})
            elif Project.objects.get(id=id).user.username != user.username:
                return Response({'error': 'You are not authorized to update this listing'})
            else:
                Project.objects.filter(id=id).update(title=title, description=description, type=type, place=place, payment=payment, target=target)
                project = Project.objects.get(id=id)
                for work in project.work_description.all():
                    project.work_description.remove(work)
                for work in work_description:
                    work = WorkDescription.objects.create(text=work['text'])
                    project.work_description.add(work)
                for reward_instance in project.reward.all():
                    project.reward.remove(reward_instance)
                for reward_instance in reward:
                    reward_instance = Reward.objects.create(text=reward_instance['text'])
                    project.reward.add(reward_instance)
                for skill in project.requirements.all():
                    project.requirements.remove(skill)
                for skill in requirements:
                    if Skill.objects.filter(name=skill["name"].lower()).exists():
                        skill_instance = Skill.objects.get(name=skill['name'].lower())
                        project.requirements.add(skill_instance)
                    else:
                        skill_instance = Skill.objects.create(name=skill['name'].lower())
                        project.requirements.add(skill_instance)
                project.save()
                serializer = ProjectSerializer(project)
                return Response({'success': 'Successfully updated listing', 'listing': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while updating listing'})


class FilterDataOfListing(APIView):

    def post(self, request, format=None):
        data = self.request.data
        skills = data['skills']
        location = data['location']
        salary = data['salary']
        salary_type = data['salary_type']
        project_serializer_list = []
        if not skills:
            if salary == "1000":
                salary = 1000
            elif salary == "5000":
                salary = 5000
            else:
                salary = 100000
            projects = Project.objects.filter(payment__lte=salary,
                                              type__icontains=salary_type, place__icontains=location).order_by(
                '-created_at')
            for project in projects:
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
                    "positions": project.positions,
                    "user": user_serializer.data,
                    "applications": applications_user_serializer.data,
                    "views": applications_views_serializer.data,
                    "requirements": skill_serializer.data,
                    "reward": rewards_serializer.data,
                    "work_description": work_serializer.data,
                }
                project_serializer_list.append(serializer)
            return Response({'listings': project_serializer_list})
        for skill in skills.split(','):
            if Skill.objects.filter(name=skill.strip().lower()).exists():
                skill_instance = Skill.objects.get(name=skill.strip().lower())
                if salary == "1000":
                    projects = Project.objects.filter(requirements=skill_instance, payment__lte=1000, type__icontains=salary_type, place__icontains=location).order_by('-created_at')
                    for project in projects:
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
                            "positions": project.positions,
                            "user": user_serializer.data,
                            "applications": applications_user_serializer.data,
                            "views": applications_views_serializer.data,
                            "requirements": skill_serializer.data,
                            "reward": rewards_serializer.data,
                            "work_description": work_serializer.data,
                        }
                        project_serializer_list.append(serializer)
                elif salary == "5000":
                    projects = Project.objects.filter(requirements=skill_instance, payment__lte=10000, place__icontains=location, type__icontains=salary_type).order_by('-created_at')
                    print(projects)
                    for project in projects:
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
                            "positions": project.positions,
                            "user": user_serializer.data,
                            "applications": applications_user_serializer.data,
                            "views": applications_views_serializer.data,
                            "requirements": skill_serializer.data,
                            "reward": rewards_serializer.data,
                            "work_description": work_serializer.data,
                        }
                        project_serializer_list.append(serializer)
                else:
                    projects = Project.objects.filter(requirements=skill_instance, payment__gte=10000, type__icontains=salary_type, place__icontains=location).order_by('-created_at')
                    for project in projects:
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
                            "positions": project.positions,
                            "user": user_serializer.data,
                            "applications": applications_user_serializer.data,
                            "views": applications_views_serializer.data,
                            "requirements": skill_serializer.data,
                            "reward": rewards_serializer.data,
                            "work_description": work_serializer.data,
                        }
                        project_serializer_list.append(serializer)
        return Response({'listings': project_serializer_list})


class GetListings(APIView):

    def get(self, request, format=None):
        try:
            projects = Project.objects.filter(completed=False, deleted=False).order_by('-created_at')
            for project in projects:
                project.views.add(self.request.user)
            serializer = ProjectSerializer(projects, many=True)
            return Response({'success': 'Successfully fetched listings', 'listings': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching listings'})


class GetRecentListings(APIView):

    def get(self, request, format=None):
        try:
            user = Account.objects.get(username=self.request.user.username)
            projects = Project.objects.filter(user=user).order_by('-created_at')[0:5]
            serializer = ProjectSerializer(projects, many=True)
            return Response({'success': 'Successfully fetched recent listings', 'listings': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching recent listings'}, status=status.HTTP_400_BAD_REQUEST)


class FetchMyListings(APIView):

    def get(self, request, format=None):
        try:
            projects = Project.objects.filter(user=self.request.user).order_by('-created_at')
            serializer = ProjectSerializer(projects, many=True)
            return Response({'success': 'Successfully fetched listings', 'listings': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching listings'}, status=status.HTTP_400_BAD_REQUEST)


class ListingAnalytics(APIView):

    def get(self, request, format=None):
        try:
            username = self.request.user.username
            user = Account.objects.get(username=username)
            dates = Project.objects.filter(user=user).order_by().values("created_at__date").distinct()
            charts_dates = []
            project_number = []
            for date in dates:
                access_date = date["created_at__date"]
                project_count = Project.objects.filter(created_at__date=access_date).count()
                charts_dates.append(access_date)
                project_number.append(project_count)
            return Response({'dates': charts_dates, 'projects': project_number})
        except:
            return Response({'error':"Error"})


class StaticticsAnalytics(APIView):

    def get(self, request, format=None):
        try:
            username = self.request.user.username
            user = Account.objects.get(username=username)
            dates = Application.objects.filter(applicant=user).order_by().values("created_at__date").distinct()
            charts_dates = []
            application_number = []
            for date in dates:
                access_date = date["created_at__date"]
                application_count = Application.objects.filter(created_at__date=access_date).count()
                charts_dates.append(access_date)
                application_number.append(application_count)
            return Response({'dates': charts_dates, 'applications': application_number})
        except:
            return Response({'error':"Error"})


class TopPerformers(APIView):

    def get(self, request, format=None):
        try:
            users = Account.objects.order_by("-points")
            serializer = AccountSerializer(users, many=True)
            return Response({'users': serializer.data})
        except:
            return Response({'error':"Error"})


class GetListingsDetailView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data['id']
            project = Project.objects.get(id=data)
            if project:
                serializer = ProjectSerializer(project)
                return Response({'success': 'Successfully fetched listing', 'listing': serializer.data})
            else:
                return Response({'error': 'This listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Something went wrong while fetching listing'}, status=status.HTTP_400_BAD_REQUEST)


class GetHiredRatings(APIView):

    def post(self, request, format=None):
        try:
            id = self.request.data['id']
            project = Project.objects.get(id=id)
            serilizer_list = []
            for application in project.applications.all():
                if application.status == 'hired':
                    user = Account.objects.get(username=application.applicant.username)
                    if not user.raters_count.filter(username=self.request.user).exists():
                        serilizer = {
                            "id": user.id,
                            "username": user.username,
                            "full_name": user.first_name+' '+user.last_name
                        }
                        serilizer_list.append(serilizer)
            return Response({'success': 'Successfully fetched ratings', 'ratings': serilizer_list})
        except:
            return Response({'error': 'Something went wrong while fetching listing'}, status=status.HTTP_400_BAD_REQUEST)


class RateUserByOrganisation(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            rate = data['rate']
            user = Account.objects.get(username=self.request.user.username)
            rate_to = Account.objects.get(id=id)
            raters_count = rate_to.raters_count.all().count()
            rate = (rate + rate_to.rate) / (raters_count + 1)
            rate_to.raters_count.add(user)
            rate_to.rate = rate
            rate_to.save()
            return Response({'success': 'Successfully rated user'})
        except:
            return Response({'error': 'Something went wrong while adding rating'}, status=status.HTTP_400_BAD_REQUEST)


class ListingDetailViewAnalytics(APIView):

    def post(self, request, format=None):
        try:
            id = self.request.data['id']
            project = Project.objects.get(id=id)
            project_list = project.applications.all()
            # applications on
            dates = project.applications.order_by().values("created_at__date").distinct()
            charts_dates = []
            application_number = []
            for date in dates:
                access_date = date["created_at__date"]
                application = project.applications.filter(created_at__date=access_date).count()
                charts_dates.append(access_date)
                application_number.append(application)
            # user badges
            badge_labels = ['Yellow', 'Red', 'Blue', 'Green', 'Pro']
            application_badges = [0, 0, 0, 0, 0]
            for application_instance in project_list:
                if application_instance.applicant.badge == 1:
                    application_badges[0] = application_badges[0] + 1
                elif application_instance.applicant.badge == 2:
                    application_badges[1] = application_badges[1] + 1
                elif application_instance.applicant.badge == 3:
                    application_badges[2] = application_badges[2] + 1
                elif application_instance.applicant.badge == 4:
                    application_badges[3] = application_badges[3] + 1
                elif application_instance.applicant.points == 5:
                    application_badges[4] = application_badges[4] + 1
            # ratings
            rates = [0, 0, 0, 0, 0]
            rating_labels = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
            for application_instance in project_list:
                print(application_instance.applicant.rate)
                if application_instance.applicant.rate == 1:
                    rates[0] = rates[0] + 1
                elif application_instance.applicant.rate == 2:
                    rates[1] = rates[1] + 1
                elif application_instance.applicant.rate == 3:
                    rates[2] = rates[2] + 1
                elif application_instance.applicant.rate == 4:
                    rates[3] = rates[3] + 1
                elif application_instance.applicant.rate == 5:
                    rates[4] = rates[4] + 1
            return Response({'dates': charts_dates, 'applications': application_number, 'badge_labels': badge_labels, 'application_badges': application_badges, 'rating_labels': rating_labels, 'rates': rates})
        except:
            return Response({'error':"Error"} ,status=status.HTTP_400_BAD_REQUEST)


class HiredInProjectAPIView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data['id']
            project = Project.objects.get(id=data)
            if project.user.username == self.request.user.username:
                user = Account.objects.get(username=self.request.user.username)
                user.points = user.points + 10
                user.save()
                project.completed = True
                project.save()
                return Response({'success': 'Successfully fetched listing'})
            else:
                return Response({'error': 'You are not authorized to this url'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong while fetching listing'})


class ApplyToListing(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            status_app = 'notviewed'
            # applying_for = data['apply']
            project = Project.objects.get(id=id)
            user = Account.objects.get(username=self.request.user.username)
            if project.applications.filter(applicant=user).exists():
                return Response({'error': 'You have already applied for this listings'}, status=status.HTTP_400_BAD_REQUEST)
            application = Application.objects.create(applicant=user, status=status_app, applying_for='all')
            user.points = user.points + 4
            user.save()
            project.applications.filter()
            project.applications.add(application)
            return Response({'success': 'Successfully Submitted Application'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Error in submitting response'})


class FetchDisplayUsersListings(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = Account.objects.get(username=data['username'])
            listings = Project.objects.filter(user=user)
            serializers = ProjectSerializer(listings, many=True)
            return Response({'listings': serializers.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Error in fetching response'}, status=status.HTTP_404_BAD_REQUEST)
