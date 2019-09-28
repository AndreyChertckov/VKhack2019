from django.contrib import admin
from .models import User, Log, Clock, Action, Fact, UserAction

# Register your models here.
admin.site.register(User)
admin.site.register(Log)
admin.site.register(Clock)
admin.site.register(Action)
admin.site.register(Fact)
admin.site.register(UserAction)