from django.contrib import admin
from .models import IncomingMessage, User, Quiz, Award, Message
# Register your models here.

admin.site.register(IncomingMessage)
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Award)
admin.site.register(Message)
