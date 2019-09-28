from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Q


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
    before = models.TimeField()
    after = models.TimeField()

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
    def usage_frequency(self):
        return self.user.logs.filter(action__id=self.action.id).annotate(count=models.Count("id"))['count']


class WeeklyLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='weekly_log')

    @property
    def weekly_log(self):
        last_7_days = datetime.datetime.today() - datetime.timedelta(7)
        return self.user.logs.filter(date_added_gte=last_7_days).extra({"day": "date_trunc('day', date_added)"})\
            .annotate(
            week_minus=models.Sum('action__time_effect', only=Q(action__time_effect__lt=0)),
            week_plus=models.Sum('action__time_effect', only=Q(action__time_effect__gt=0)))


class MonthlyLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='monthly_log')

    @property
    def monthly_log(self):
        last_30_days = datetime.datetime.today() - datetime.timedelta(30)
        return self.user.logs.filter(date_added_gte=last_30_days).extra({"day": "date_trunc('day', date_added)"}) \
            .annotate(
            month_minus=models.Sum('action__time_effect', only=Q(action__time_effect__lt=0)),
            month_plus=models.Sum('action__time_effect', only=Q(action__time_effect__gt=0)))


class Fact(models.Model):
    description = models.TextField()
    appearance_time = models.TimeField()
