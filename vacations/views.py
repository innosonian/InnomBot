import json
from datetime import date, datetime

import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .form_maker import generate_from_data, get_vacation_apply_form, get_half_vacation_apply_form, \
    get_invalid_date_alarm_form, \
    get_not_selected_vacation_type_alarm_form, get_vacation_apply_success_form, get_vacation_apply_success_alarm
from .models import Vacation, User, VacationType


SLACK_URL = 'https://hooks.slack.com/services/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'

@api_view(["POST"])
def vacation_get(request):
    user = User.objects.get(id=request.data.get('user_id'))
    vacation = Vacation.objects.filter(user=user, deleted_at=None).order_by('-start_date')
    serializer = VacationSerializer(vacation, many=True)
    form = generate_from_data(serializer.data, user)
    print("form:::", form)
    return Response(data=form, status=status.HTTP_200_OK)


@api_view(["POST"])
def vacation_create_form(request):
    form = get_vacation_apply_form()
    return Response(data=form, status=status.HTTP_200_OK)


def is_click_apply_button(data):
    return data['actions'][0]['action_id'] == 'vacation_apply'


def is_change_vacation_type(data):
    return data['actions'][0]['action_id'] == 'vacation_type'


def is_not_select_vacation_type(data):
    return data['state']['values']['vacation_type_id']['vacation_type']['selected_option'] is None


def is_day_off(data):
    return data['actions'][0]['selected_option']['value'] == '1'


@api_view(["POST"])
def vacation_apply(request):
    data = json.loads(request.data['payload'])
    print(data)

    if is_click_apply_button(data):
        user = data['user']['id']
        start_date = data['state']['values']['date_id']['start_date']['selected_date']
        end_date = data['state']['values']['date_id']['end_date']['selected_date'] if 'end_date' in \
                                                                                      data['state']['values'][
                                                                                          'date_id'] else start_date
        message = data['state']['values']['message_id']['message']['value']
        if is_not_select_vacation_type(data):
            requests.post(data['response_url'], json=get_not_selected_vacation_type_alarm_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)
        if end_date != '' and start_date > end_date:
            requests.post(data['response_url'], json=get_invalid_date_alarm_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)

        vacation_type = data['state']['values']['vacation_type_id']['vacation_type']['selected_option']['value']

        user = User.objects.get(id=user)
        vacation_type = VacationType.objects.get(id=vacation_type)

        Vacation.objects.create(user=user, vacation_type=vacation_type, start_date=start_date, end_date=end_date,
                                message=message)

        requests.post(data['response_url'], json=get_vacation_apply_success_form())
        res = requests.post(SLACK_URL, json=get_vacation_apply_success_alarm(user, vacation_type, start_date, end_date=end_date))
        print(res.content)
        return Response({'message': res.status_code}, status=status.HTTP_200_OK)
    elif is_change_vacation_type(data):
        if is_day_off(data):
            requests.post(data['response_url'], json=get_vacation_apply_form())
            return Response(data=get_vacation_apply_form(), status=status.HTTP_200_OK)
        else:
            requests.post(data['response_url'], json=get_half_vacation_apply_form())
            return Response(data=get_half_vacation_apply_form(), status=status.HTTP_200_OK)
    elif 'vacation_delete' in data['actions'][0]['action_id']:
        vacation_id = data['actions'][0]['action_id'].split('_')[2]
        Vacation.objects.filter(id=vacation_id).update(deleted_at=datetime.now())
        user = User.objects.get(id=data['user']['id'])
        vacation = Vacation.objects.filter(user=user, deleted_at=None).order_by('-start_date')
        serializer = VacationSerializer(vacation, many=True)
        form = generate_from_data(serializer.data, user)
        requests.post(data['response_url'], json=form)
        return Response({'message': f'{vacation_id} 해당 휴가 삭제'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '무시해'}, status=status.HTTP_200_OK)
