from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation, User
from datetime import datetime, date
import dateutil.parser

def timezone_parser(timezone_data):
    days = ['월(Mon)','화(Tue)','수(Wed)','목(Thu)','금(Fri)','토(Sat)','일(Sun)']
    dt_parse = dateutil.parser.parse(timezone_data)
    dt_form = dt_parse.year, dt_parse.month, dt_parse.day
    day = date(dt_parse.year, dt_parse.month, dt_parse.day).weekday()
    final_format = f"{dt_form[0]}.{dt_form[1]}.{dt_form[2]} {days[day]}"
    print("final_format::::", final_format )

    return final_format

class VacationAPI(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data.get('user_id'))
        vacation = Vacation.objects.filter(user=user)
        serializer = VacationSerializer(vacation, many=True)
        result = list()
        for data in serializer.data:
            vacation_format = timezone_parser(data.get('date'))
            print("vacation_format::::", vacation_format)
            result.append(vacation_format)

        vacations = '\n'.join(result)
        form = {
            "channel": "D04BJFUAQFR",
            "response_type": "in_channel",
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
        return Response(data=form, status=status.HTTP_200_OK)
