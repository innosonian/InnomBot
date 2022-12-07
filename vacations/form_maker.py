from datetime import datetime, date

from vacations.models import VacationType

DAY_OFF = 1


def day_of_date(date_format):
    days = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
    day_num = date_format.weekday()
    return days[day_num]


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

        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        start_day = day_of_date(start_date)
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        end_day = day_of_date(end_date)

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
