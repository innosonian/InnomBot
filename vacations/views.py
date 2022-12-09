import json

import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from datetime import datetime, date
from .form_maker import generate_from_data, get_vacation_apply_form
from .models import Vacation, User, VacationType


def timezone_parser(timezone_data):
    days = ['월(Mon)','화(Tue)','수(Wed)','목(Thu)','금(Fri)','토(Sat)','일(Sun)']
    dt_parse = dateutil.parser.parse(timezone_data)
    dt_form = dt_parse.year, dt_parse.month, dt_parse.day
    day = date(dt_parse.year, dt_parse.month, dt_parse.day).weekday()
    final_format = f"{dt_form[0]}.{dt_form[1]}.{dt_form[2]} {days[day]}"
    print("final_format::::", final_format )

    return final_format

@api_view(["POST"])
def vacation_get(request):
    user = User.objects.get(id=request.data.get('user_id'))
    vacation = Vacation.objects.filter(user=user).order_by('-start_date')
    serializer = VacationSerializer(vacation, many=True)
    form = generate_from_data(serializer.data, user)
    print("form:::", form)
    return Response(data=form, status=status.HTTP_200_OK)


@api_view(["POST"])
def vacation_create_form(request):
    form = get_vacation_apply_form()
    return Response(data=form, status=status.HTTP_200_OK)


@api_view(["POST"])
def vacation_apply(request):
    data = json.loads(request.data['payload'])
    if data['actions'][0]['action_id'] == 'vacation_apply':
        user = data['user']['id']
        vacation_type = data['state']['values']['vacation_type_id']['vacation_type']['selected_option']['value']
        start_date = data['state']['values']['date_id']['start_date']['selected_date']
        end_date = data['state']['values']['date_id']['end_date']['selected_date']
        message = data['state']['values']['message_id']['message']['value']

        if start_date > end_date:
            return Response({'message': '무시해'}, status=status.HTTP_200_OK)

        user = User.objects.get(id=user)
        vacation_type = VacationType.objects.get(id=vacation_type)

        Vacation.objects.create(user=user, vacation_type=vacation_type, start_date=start_date, end_date=end_date,
                                message=message)
        form = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "휴가 요청이 성공했습니다",
                    }
                }
            ]
        }
        res = requests.post(data['response_url'], json=form)
        return Response({'message': res.status_code}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '무시해'}, status=status.HTTP_200_OK)
