from django.db import models
from django.utils import timezone


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

    def create(self):
        self.time = timezone.now()
        self.save()



