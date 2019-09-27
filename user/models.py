from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    name = models.CharField(max_length=200, default="Arina")
    clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name='user')

    def create(self, data):
        self.name = data['name']
        self.clock = data['clock']
        self.save()


class Clock(models.Model):
    time = models.TimeField()

    @property
    def daily_minus(self):
        return self.user.first().logs.filter(action__time_effect__lt=0).aggregate(daily_minus=models.Sum('action__time_effect'))['daily_minus']

    @property
    def daily_plus(self):
        return self.user.first().logs.filter(action__time_effect__gt=0).aggregate(daily_plus=models.Sum('action__time_effect'))['daily_plus']

    def create(self, data):
        self.time = data['time']
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
        current = self.user.clock.time
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
        for i in range(0, 7):
            week[(current - datetime.timedelta(days=(i + 1)))] = [0, 0]
        for day in week:
            for log in self.user.logs:
                if log.time.date() == day:
                    if log.action.time_effect > 0:
                        week[day][0] += log.action.time_effect
                    else:
                        week[day][1] += log.action.time_effect
        return week


class MonthlyLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='monthly_log')

    @property
    def monthly_log(self):
        current = datetime.date.today()
        month = {}
        for i in range(0, 30):
            month[(current - datetime.timedelta(days=(i + 1)))] = [0, 0]
        for day in month:
            for log in self.user.logs:
                if log.time.date() == day:
                    if log.action.time_effect > 0:
                        month[day][0] += log.action.time_effect
                    else:
                        month[day][1] += log.action.time_effect
        return month


class Fact(models.Model):
    description = models.TextField()
    appearance_time = models.TimeField()
