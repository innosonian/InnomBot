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
            "channel": "D04BJFUAQFR",
            "attachments": [{
                "color": "#2eb886",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{user.name}* 님의 휴가 사용 내역: *{len(vacation)}*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{vacations}"
                        }
                    },
                    {
                        "type": "section",
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "사용 완료",
                            },
                            "style": "primary"
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "2022.11.21 (금) - 1일"
                        }
                    },
                    {
                        "type": "section",
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "사용 완료",
                            },
                            "style": "primary"
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "2022.11.21 (금) ~ 11.22 (토) - 2일"
                        }
                    }
                ]
            }]
        }
        return Response(form, status.HTTP_200_OK)
