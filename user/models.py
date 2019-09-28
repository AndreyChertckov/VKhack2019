from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    name = models.CharField(max_length=200, default="Arina")
    token = models.CharField(default='')
    smoke = models.BooleanField()
    alcohol = models.BooleanField()
    clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name='user')

    def create(self, data):
        self.name = data['name']
        self.clock = data['clock']
        self.save()


class Clock(models.Model):
    time = models.TimeField()

    @property
    def daily_minus(self):
        return self.user.first().logs.filter(action__time_effect__lt=0, time__date=datetime.date.today()).aggregate(daily_minus=models.Sum('action__time_effect'))['daily_minus']

    @property
    def daily_plus(self):
        return self.user.first().logs.filter(action__time_effect__gt=0, time__date=datetime.date.today()).aggregate(daily_plus=models.Sum('action__time_effect'))['daily_plus']

    def create(self, data):
        self.time = data['time']
        self.save()


class Action(models.Model):
    name = models.CharField(max_length=200)
    time_effect = models.IntegerField()
    users = models.ManyToManyField(User, related_name='actions', through='UserAction')
    description = models.CharField(max_length=380)


class Log(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='logs')
    time = models.DateTimeField()
    action = models.ForeignKey(Action, null=True, on_delete=models.CASCADE, related_name='logs')
    before = models.TimeField(default=datetime.time(0, 0, 0))
    after = models.TimeField(default=datetime.time(0, 0, 0))

    def create(self, data):
        self.user = data['user']
        self.action = data['action']
        self.time = timezone.now()
        if self.action.time_effect > 0:
            self.before = (self.user.clock.time - datetime.time(minute=self.action.time_effect)).time()
        else:
            self.before = (self.user.clock.time + datetime.time(minute=((-1) * self.action.time_effect))).time()
        self.after = self.user.clock.time
        self.save()


class UserAction(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_actions')
    action = models.ForeignKey(Action, null=True, on_delete=models.CASCADE, related_name='user_actions')

    @property
    def frequency(self):
        return self.user.logs.filter(action__id=self.action.id).aggregate(count=models.Count("id"))['count']

class Fact(models.Model):
    description = models.TextField()
    appearance_time = models.TimeField()
