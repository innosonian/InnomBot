from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation, User


class VacationAPI(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data.get('user_id'))
        vacation = Vacation.objects.filter(user=user)
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
                        "text": f""
                                f"{user.name}님의 휴가 사용 현황: {len(vacation)}"
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
