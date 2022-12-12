from rest_framework import serializers

from vacations.models import Vacation, User


class VacationSerializer(serializers.ModelSerializer):
    order_by = ('start_date', )

    class Meta:
        model = Vacation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
