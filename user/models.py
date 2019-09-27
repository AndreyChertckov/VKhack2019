from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    clock = models.TimeField()

    @property
    def daily_minus(self):
        return filter(lambda x: x.action.time_effect < 0, self.logs)

    @property
    def daily_plus(self):
        return filter(lambda x: x.action.time_effect > 0, self.logs)

    def create(self):
        self.save()


class Action(models.Model):
    name = models.CharField(max_length=200)
    time_effect = models.IntegerField()


class Log(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='logs')
    time = models.DateTimeField()
    action = models.ForeignKey(Action, null=True, on_delete=models.CASCADE, related_name='logs')

    @property
    def before(self):
        current = self.user.clock
        for log in self.user.logs:
            if log.time > self.time:
                if log.action.time_effect > 0:
                    current = (current - datetime.timedelta(minutes=log.action.time_effect)).time()
                else:
                    current = (current + datetime.timedelta(minutes=((-1) * log.action.time_effect))).time()
        return current

    @property
    def after(self):
        if self.action.time_effect > 0:
            return (self.before + datetime.timedelta(minutes=self.action.time_effect)).time()
        else:
            return (self.before - datetime.timedelta(minutes=((-1) * self.action.time_effect))).time()

    def create(self):
        self.time = timezone.now()
        self.save()


class Fact(models.Model):
    description = models.TextField()
    appearance_time = models.TimeField()
