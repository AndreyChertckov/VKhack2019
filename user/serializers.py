from rest_framework import serializers
from user.models import User, Clock, Action, Log, UserAction, Fact


class ClockSerializer(serializers.ModelSerializer):
    daily_minus = serializers.ReadOnlyField()
    daily_plus = serializers.ReadOnlyField()
    class Meta:
        model = Clock
        fields = ['time', 'daily_minus', 'daily_plus']

    def create(self, validated_data):
        return Clock.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    clock = ClockSerializer(allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'vk_id', 'clock', 'token', 'drinking', 'smoking']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['name', 'time_effect', 'description']


class LogSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    class Meta:
        model = Log
        fields = ['time', 'before', 'after', 'action']


class UserActionSerializer(serializers.ModelSerializer):
    frequency = serializers.ReadOnlyField()
    action = ActionSerializer()
    class Meta:
        model = UserAction
        fields = ['action','user','frequency']


class FactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fact
        fields = ['description']