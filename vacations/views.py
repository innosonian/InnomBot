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
        total_vacations = list()

        # 각 휴가의 사용 일자 총합을 구하기 번거로우니 '사용일수' 컬럼을 하나 파면 어떨까? 휴가 신청 시에 연산해서 테이블에 담고 -> 모델에서 가져와서 sum만 하면 되도록
        # 현재는 list 새로 파고 for문을 따로 돌려서 sum하는 형식(user_data_form, divider가 하위 for문 안에서 같이 돌면 안되고, user_data_form에 sum값을 주어야 해서)
        # for difference in serializer.data:
        #     cal_vacations = (date_formatter(difference.get('end_date')) - date_formatter(difference.get('start_date'))).days + 1
        #     total_vacations.append(cal_vacations)

        section_text = { "type" : "mrkdwn", "text": ""}
        user_data_form = { "type" : "section", "text" : section_text }
        # user_data_form = {
        #     "type": "section",
        #     "text": {
        #         "type": "mrkdwn",
        #         "text": f"*{user.name}* 님의 휴가 사용 내역: 총 *{len(vacation)}* 건, 사용 일수: 총 *{sum(total_vacations)}* 일"
        #     }
        # }
        divider = {
            "type": "divider"
        }
        result.append(user_data_form)
        result.append(divider)

        # button_text = {"type": "plain_text", "text": ""}
        # button = {"type": "button", "text": button_text}
        # vacation_form = {"type": "mrkdwn", "text": ""}
        # vacation_list_form = {"type": "section", "accessory": button, "text": vacation_form}

        for data in serializer.data:
            start_date = date_formatter(data.get('start_date'))
            start_day = day_of_date(start_date)
            end_date = date_formatter(data.get('end_date'))
            end_day = day_of_date(end_date)

            cal_vacations = (end_date - start_date).days + 1  # 반환형식: 숫자
            total_vacations.append(cal_vacations)
            section_text['text'] = f"*{user.name}* 님의 휴가 사용 내역: 총 *{len(vacation)}* 건, 사용 일수: 총 *{sum(total_vacations)}* 일"

            globals()['button_text{}'.format(data.get('id'))] = {"type": "plain_text", "text": ""}
            globals()['button{}'.format(data.get('id'))] = {"type": "button", "text": globals()['button_text{}'.format(data.get('id'))]}
            globals()['vacation_form{}'.format(data.get('id'))] = {"type": "mrkdwn", "text": ""}
            globals()['vacation_list_form{}'.format(data.get('id'))] = {"type": "section",
                                                                        "accessory": globals()['button{}'.format(data.get('id'))],
                                                                        "text": globals()['vacation_form{}'.format(data.get('id'))]}

            result.append(globals()['vacation_list_form{}'.format(data.get('id'))])

            try:
                if datetime.today() >= datetime(start_date.year, start_date.month, start_date.day, hour=11):
                    globals()['vacation_list_form{}'.format(data.get('id'))]["accessory"]["text"]["text"] = "사용완료"
                else:
                    globals()['vacation_list_form{}'.format(data.get('id'))]["accessory"]["text"]["text"] = "사용대기"
                    button_style = {"style" : "primary"}
                    globals()['vacation_list_form{}'.format(data.get('id'))]["accessory"].update(button_style)
            except:
                print("error, 날짜 데이터 연산에 실패했습니다. 데이터를 확인해 주세요.")

            finally:
                if start_date == end_date:
                    print("start_date == end_date 몇번 타나")
                    print("data.get('id'):::::", data.get('id'))
                    # 기존 코드2
                    # globals()['vacation_list_form{}'.format(data.get('id'))] = {"type": "section", "accessory": button,
                    #                                                                         "text": vacation_form}
                    #  result.append(globals()['vacation_list_form{}'.format(data.get('id'))])
                    globals()['vacation_list_form{}'.format(data.get('id'))]["text"]["text"] = f"{start_date}{start_day} - {cal_vacations}day"
                    print(f"vacation_list_form_{data.get('id')}:::::", globals()['vacation_list_form{}'.format(data.get('id'))])

                    # 기존 코드1
                    # vacation_form["text"] = f"{start_date}{start_day} - {cal_vacations}day"
                    # print("== vacation_list_form :::/n", vacation_list_form)
                    # result.append(vacation_list_form)

                else:
                    print("start_date <> end_date 몇번 타나")
                    print("data.get('id'):::::", data.get('id'))
                    # 기존 코드2
                    # globals()['vacation_list_form{}'.format(data.get('id'))] = {"type": "section", "accessory": button,
                    #                                                             "text": vacation_form}
                    # result.append(globals()['vacation_list_form{}'.format(data.get('id'))])
                    globals()['vacation_list_form{}'.format(data.get('id'))]["text"]["text"] = f"{start_date}{start_day} ~ {end_date}{end_day} - {cal_vacations}days "
                    print(f"vacation_list_form_{data.get('id')}:::::", globals()['vacation_list_form{}'.format(data.get('id'))])


                    # 기존 코드1
                    # vacation_form["text"] = f"{start_date}{start_day} ~ {end_date}{end_day} - {cal_vacations}days "
                    # print("<> vacation_list_form :::/n", vacation_list_form)
                    # result.append(vacation_list_form)

        # result가 list여서 꺼내는게 문제였는데, 반대로 리스트인걸 이용하기로 함("blocks" 키 값의 value를 리스트[]로 싸는 형식이라 거기서 result를 불러준다.
        form = {
            "response_type": "in_channel",
            "attachments": [{
                "color": "#2eb886",
                "blocks": result
            }]
        }
        print("form:::", form)
        return Response(data=form, status=status.HTTP_200_OK)


