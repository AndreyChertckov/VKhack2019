from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    name = models.CharField(max_length=200)
    clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name='user')

    def create(self):
        self.save()


class Clock(models.Model):
    time = models.TimeField()

    @property
    def daily_minus(self):
        return filter(lambda x: x.action.time_effect < 0, self.logs)

    @property
    def daily_plus(self):
        return filter(lambda x: x.action.time_effect > 0, self.logs)


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


class UserAction(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_actions')
    action = models.ForeignKey(Action, null=True, on_delete=models.CASCADE, related_name='user_actions')

    @property
    def usage_frequency(self):
        n = 0
        for log in self.user.logs:
            if log.action.id == self.action.id:
                n += 1
        return n


class WeeklyLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='weekly_log')

    @property
    def weekly_log(self):
        current = datetime.date.today()
        week = {}




class Fact(models.Model):
    description = models.TextField()
    appearance_time = models.TimeField()
