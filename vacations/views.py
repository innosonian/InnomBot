import json

import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation, User, VacationType
from datetime import datetime, date
import dateutil.parser

DAY_OFF = 1


def date_formatter(timezone_data):
    dt_parse = dateutil.parser.parse(timezone_data)
    date_format = date(dt_parse.year, dt_parse.month, dt_parse.day)
    return date_format


def day_of_date(date_format):
    days = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
    day_num = date_format.weekday()
    day = days[day_num]
    return day


@api_view(["POST"])
def vacation_get(request):
    user = User.objects.get(id=request.data.get('user_id'))
    vacation = Vacation.objects.filter(user=user).order_by('-start_date')
    serializer = VacationSerializer(vacation, many=True)
    form = generate_from_data(serializer.data, user)
    print("form:::", form)
    return Response(data=form, status=status.HTTP_200_OK)


def generate_from_data(serialized_vacation, user):
    result = list()
    total_vacations = list()

    section_text = {"type": "mrkdwn", "text": ""}
    user_data_form = {"type": "section", "text": section_text}
    divider = {"type": "divider"}
    result.append(user_data_form)
    result.append(divider)

    for data in serialized_vacation:
        button_text = {"type": "plain_text", "text": ""}
        button = {"type": "button", "text": button_text}
        vacation_form = {"type": "mrkdwn", "text": ""}
        vacation_list_form = {"type": "section", "accessory": button, "text": vacation_form}

        start_date = date_formatter(data.get('start_date'))
        start_day = day_of_date(start_date)
        end_date = date_formatter(data.get('end_date'))
        end_day = day_of_date(end_date)

        # 각 휴가의 사용 일자 연산이 조회에서만 필요한가? vacation table에 '사용일수' 컬럼을 하나 파면 어떨까?
        # 휴가 신청 시에 연산해서 테이블에 담고 -> 모델에서 가져와서 sum만 하면 되도록
        vacation_type = VacationType.objects.get(id=data.get('vacation_type'))
        if vacation_type.id == DAY_OFF:
            cal_vacations = int((end_date - start_date).days + vacation_type.weight)  # 반환형식: 숫자
        else:
            cal_vacations = vacation_type.weight
        total_vacations.append(cal_vacations)

        if datetime.today() >= datetime(start_date.year, start_date.month, start_date.day, hour=11):
            button_text["text"] = "사용완료"

        else:
            button_text["text"] = "사용대기"
            button_style = {"style": "primary"}
            button.update(button_style)

        if start_date == end_date:
            vacation_form["text"] = f"{start_date}{start_day} - {cal_vacations}day"
            result.append(vacation_list_form)

        else:
            vacation_form["text"] = f"{start_date}{start_day} ~ {end_date}{end_day} - {cal_vacations}days"
            result.append(vacation_list_form)

    section_text[
        'text'] = f"*{user.name}* 님의 휴가 사용 내역: 총 *{len(serialized_vacation)}* 건, 사용 일수: 총 *{sum(total_vacations)}* 일"

    # result가 list여서 꺼내는게 문제였는데, 반대로 리스트인걸 이용하기로 함
    # "blocks" 키 값의 value를 리스트[]로 싸는 형식이라 거기서 result를 불러준다.
    form = {
        "response_type": "in_channel",
        "attachments": [{
            "color": "#2eb886",
            "blocks": result
        }]
    }
    return form


def generate_payload(data):
    return data


@api_view(["POST"])
def vacation_create_form(request):
    form = get_vacation_apply_form()
    print(form)
    return Response(data=form, status=status.HTTP_200_OK)


def get_vacation_type():
    vacation_type = VacationType.objects.all()
    result = list()
    for item in vacation_type:
        s = {
            "text": {
                "type": "plain_text",
                "text": item.name,
            },
            "value": f"{item.id}"
        }
        result.append(s)
    return result


def get_vacation_apply_form():
    return {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "휴가 신청서(Request For Vacation)",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*휴가 종류(Vacation Type)*"
                }
            },
            {
                "type": "actions",
                "block_id": "vacation_type_id",
                "elements": [
                    {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                        },
                        "options": get_vacation_type(),
                        "action_id": "vacation_type"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*휴가 일정(Vacation Schedule)*"
                }
            },
            {
                "type": "actions",
                "block_id": "date_id",
                "elements": [
                    {
                        "type": "datepicker",
                        "initial_date": date.today(),
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                        },
                        "action_id": "start_date"
                    },
                    {
                        "type": "datepicker",
                        "initial_date": date.today(),
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                        },
                        "action_id": "end_date"
                    }
                ]
            },
            {
                "type": "input",
                "block_id": "message_id",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "message"
                },
                "label": {
                    "type": "plain_text",
                    "text": "메시지(Message)",
                }
            },
            {
                "text": {
                    "type": "mrkdwn",
                    "text": " "
                },
                "type": "section",
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "전송",
                    },
                    "style": "primary",
                    "value": "apply",
                    "action_id": "vacation_apply"
                }
            }
        ]
    }


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
                        "text": "휴가 요청이 성공적으로 등록되었습니다.",
                    }
                }
            ]
        }
        res = requests.post(data['response_url'], json=form)
        return Response({'message': res.status_code}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '무시해'}, status=status.HTTP_200_OK)
