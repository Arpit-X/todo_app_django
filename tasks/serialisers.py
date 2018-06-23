from .models import *
from rest_framework import serializers


class TaskSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','subject','desciption','deadline','time_created')


