from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .models import Vacation, User, VacationType
from datetime import datetime, date
import dateutil.parser
import json
DAY_OFF = 1

def date_formatter(timezone_data):
    dt_parse = dateutil.parser.parse(timezone_data)
    date_format = date(dt_parse.year, dt_parse.month, dt_parse.day)
    return date_format


def day_of_date(date_format):
    days = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
    day_num = date_format.weekday()
    day= days[day_num]
    return day


class VacationAPI(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data.get('user_id'))
        vacation = Vacation.objects.filter(user=user)
        serializer = VacationSerializer(vacation, many=True)
        form = self.generate_from_data(serializer.data, user)
        print("form:::", form)
        return Response(data=form, status=status.HTTP_200_OK)

    def generate_from_data(self, serialized_vacation, user):
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

        section_text['text'] = f"*{user.name}* 님의 휴가 사용 내역: 총 *{len(serialized_vacation)}* 건, 사용 일수: 총 *{sum(total_vacations)}* 일"

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

    def generate_payload(self, data):
        return data


