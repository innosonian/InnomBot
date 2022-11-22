from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation


class VacationAPI(APIView):
    def post(self, request):
        all = Vacation.objects.values('user_name', 'date')
        count = len(all)
        form = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"OOO님의 휴가 사용 현황:{count}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "15일 중 10일 사용하셨습니다. 남은 휴가 일수는 5일 입니다."
                    }
                }
            ]
        }
        return Response(form, status.HTTP_200_OK)
