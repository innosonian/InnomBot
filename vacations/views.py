import json

import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .form_maker import generate_from_data, get_vacation_apply_form, get_half_vacation_apply_form, get_invalid_date_alarm_form, \
    get_not_selected_vacation_type_alarm_form
from .models import Vacation, User, VacationType


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
    user = data['user']['id']
    start_date = data['state']['values']['date_id']['start_date']['selected_date']
    end_date = data['state']['values']['date_id']['end_date']['selected_date'] if 'end_date' in data['state']['values']['date_id'] else ''
    message = data['state']['values']['message_id']['message']['value']
    if data['actions'][0]['action_id'] == 'vacation_apply':
        if data['state']['values']['vacation_type_id']['vacation_type']['selected_option'] is None:
            requests.post(data['response_url'], json=get_not_selected_vacation_type_alarm_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)
        if start_date > end_date:
            requests.post(data['response_url'], json=get_invalid_date_alarm_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)

        vacation_type = data['state']['values']['vacation_type_id']['vacation_type']['selected_option']['value']

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
    elif data['actions'][0]['action_id'] == 'vacation_type':
        if data['actions'][0]['selected_option']['value'] == '1':
            form = get_vacation_apply_form()
            requests.post(data['response_url'], json=form)
            return Response(data=get_vacation_apply_form(), status=status.HTTP_200_OK)
        else:
            requests.post(data['response_url'], json=get_half_vacation_apply_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)
    else:
        return Response({'message': '무시해'}, status=status.HTTP_200_OK)
