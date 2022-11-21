from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class VacationAPI(APIView):
    def get(self, request):
        return Response({"message": "휴가 사용량은 ~개 입니다."}, status.HTTP_200_OK)
