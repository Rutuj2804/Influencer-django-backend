from rest_framework.views import APIView
from rest_framework import status
from .models import TimeSpend
from accounts.models import Account
from rest_framework.response import Response


class CreateTimeSpend(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            time = data['time']
            if time == 0:
                return Response({'success': 'Successfully Recorded Time Spend'}, status=status.HTTP_201_CREATED)
            user = Account.objects.get(username=self.request.user.username)
            TimeSpend.objects.create(user=user, time=time)
            return Response({'success': 'Successfully Recorded Time Spend'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error':'Something went wrong while recording time spend'}, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsTimeSpend(APIView):

    def get(self, request, format=None):
        try:
            username = self.request.user.username
            user = Account.objects.get(username=username)
            dates = TimeSpend.objects.filter(user=user).order_by().values("created_at__date").distinct()
            charts_dates = []
            time_spend = []
            for date in dates:
                access_date = date["created_at__date"]
                time_elements = TimeSpend.objects.filter(created_at__date=access_date)
                time = 0
                for time_element in time_elements:
                    time = time_element.time + time
                charts_dates.append(access_date)
                time_spend.append(time)
            return Response({'dates': charts_dates, 'time': time_spend}, status=status.HTTP_200_OK)
        except:
            return Response({'error':'Something went wrong while fetching time spend'}, status=status.HTTP_400_BAD_REQUEST)