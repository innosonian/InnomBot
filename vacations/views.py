from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation


class VacationAPI(APIView):
    def post(self, request):
        vacation = Vacation.objects.filter(user=request.data.get('user_id'))
        serializer = VacationSerializer(vacation, many=True)
        result = list()
        for data in serializer.data:
            vacation_format = data.get('date')
            result.append(vacation_format)
        vacations = '\n'.join(result)
        form = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"OOO님의 휴가 사용 현황:{len(vacation)}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{vacations}"
                    }
                },
            ]
        }
        return Response(form, status.HTTP_200_OK)
