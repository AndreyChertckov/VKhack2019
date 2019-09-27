from rest_framework import serializers
from user.models import User, Clock, Action, Log, Fact


class UserSerializer(serializers.ModelSerializer):
    clock = serializers.PrimaryKeyRelatedField(queryset=Clock.objects.all())
    class Meta:
        model = User
        fields = ['id', 'name', 'clock']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ClockSerializer(serializers.ModelSerializer):
    daily_minus = serializers.ReadOnlyField()
    daily_plus = serializers.ReadOnlyField()
    class Meta:
        model = Clock
        fields = ['time', 'daily_minus', 'daily_plus']

    def create(self, validated_data):
        return Clock.objects.create(**validated_data)


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ['name', 'time_effect']


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fileds = ['time', 'action', 'before', 'after']


class FactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fact
        fields = ['description']