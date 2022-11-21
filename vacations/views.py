from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer
from .slack import slack_notify
from .models import Vacation

inoToken = 'xoxb-8350808791-4401369739906-70fttnctA2TbKMsI0F7TSYcj' #공개저장소에 공개되지 않도록 주의

class VacationAPI(APIView):
    def get(self, request):
        all = Vacation.objects.values('user_name', 'date')
        count = len(all)
        check_using_vacation = "휴가 사용량은 총 {}개 입니다.".format(count)
        slack_notify(inoToken, "C04CHP6RD2L", check_using_vacation)

        return Response({"message": "휴가 사용량은 ~개 입니다."}, status.HTTP_200_OK)

    def post(self, request):
        #slack_notify(inoToken, "C04CHP6RD2L", "TEST용 알림")
        serializer = VacationSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            slack_notify(inoToken, "C04CHP6RD2L", "저장에 성공했습니다.")
            return Response(serializer.data, status.HTTP_201_CREATED)
        slack_notify(inoToken, "C04CHP6RD2L", "잘못된 요청입니다.")
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
