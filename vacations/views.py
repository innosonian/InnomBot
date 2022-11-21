from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vacations.serializers import VacationSerializer


class VacationAPI(APIView):
    def get(self, request):
        return Response({"message": "휴가 사용량은 ~개 입니다."}, status.HTTP_200_OK)

    def post(self, request):
        serializer = VacationSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
