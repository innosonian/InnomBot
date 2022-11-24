from django.test import Testcase, Client

import json

from .models import Vacation, User

# 설정한 엔드 포인트 경로를 통해 함수를 호출. request나 http와 비슷한 일
client = Client()

# 테스트 케이스를 만들 때는 항상 TestCase() 객체를 상속받아 새로운 테스트 클래스를 생성
class VacationTest(Tast):
    # 테스트 함수는 test_ 를 붙여 줘야 테스트 함수로 인식
    def test_check_vacation_post_success(self):
        # 테스트를 위해 request가 가지고 있는 data를 임의로 만들어 준다.
        data = {
            'user_id'   :   'U04ARD6H3PU'
        }

        # post 함수에 대한 테스트이기 때문에 post로 작성.
        response = client.post('/vacations', json.dumps(data), content_type= 'application/json')

        # 반환되는 status_code와 message가 같은지 비교하여 같을 경우 테스트에서 OK를 띄워준다.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "SUCCESS"
        })