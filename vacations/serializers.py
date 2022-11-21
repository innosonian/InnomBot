from rest_framework import serializers

from vacations.models import Vacation


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'
