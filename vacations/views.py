from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation, User
from datetime import datetime, date
import dateutil.parser
import json

def date_formatter(timezone_data):
    dt_parse = dateutil.parser.parse(timezone_data)
    date_format = date(dt_parse.year, dt_parse.month, dt_parse.day)
    return date_format

def day_of_date(date_format):
    days = ['(월)','(화)','(수)','(목)','(금)','(토)','(일)']
    day_num = date_format.weekday()
    day= days[day_num]
    return day

class VacationAPI(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data.get('user_id'))
        vacation = Vacation.objects.filter(user=user)
        serializer = VacationSerializer(vacation, many=True)
        result = list()
        user_data_form = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{user.name}* 님의 휴가 사용 내역: 총 *{len(vacation)}* 건"
            }
        }
        devider = {
            "type": "divider"
        }
        result.append(user_data_form)
        result.append(devider)
        for data in serializer.data:
            start_date = date_formatter(data.get('start_date'))
            start_day = day_of_date(start_date)
            end_date = date_formatter(data.get('end_date'))
            end_day = day_of_date(end_date)

            if start_date == end_date:
                vacation_form = {
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
                            "text": f"{start_date} {start_day} - 1일"
                        }
                    }
                result.append(vacation_form)
            else:
                # 일자 계산은 아직 더 다듬어야 함
                # cal_vacations = end_date - start_date  # 반환형식: 1 day, 0:00:00
                vacation_form = {
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
                            "text": f"{start_date} {start_day} ~ {end_date} {end_day} - 2일간 "
                        }
                    }
                print("vacation_form type:::::", type(vacation_form))
                result.append(vacation_form)
        # list로 반환되는 것이 문제였는데, 반대로 이용하기로 함( "blocks" 키 값의 value를 리스트[]로 싸는 형식이라 거기서 result를 불러준다.
        form = {
            "response_type": "in_channel",
            "attachments": [{
                "color": "#2eb886",
                "blocks": result
            }]
        }
        return Response(data=form, status=status.HTTP_200_OK)
