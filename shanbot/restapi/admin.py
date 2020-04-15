from django.contrib import admin
from .models import IncomingMessage, User, Quiz, Award, Message, Secret, WrongAward
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'first_name', 'state',
                    'created_at', 'last_quiz_solve', 'solving_mode')
    actions = ['make_published']

    def make_published(self, request, queryset):
        a = []
        for obj in queryset:
            if (obj.last_quiz_solve+1) == 10:
                a += [obj.vk_id]
        g = 9
        

    make_published.short_description = "Mark selected stories as published"


admin.site.register(User, UserAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('order', 'text',
                    'available_strtime', 'available_unixtime')


admin.site.register(Quiz, QuizAdmin)


class AwardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'attachments_json')


admin.site.register(Award, AwardAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_type', 'text', 'attachments_json')


admin.site.register(Message, MessageAdmin)


class SecretAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'available',
                    'order_type', 'attachments_json')


admin.site.register(Secret, SecretAdmin)


admin.site.register(IncomingMessage)



class WrongAwardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'attachments_json')


admin.site.register(WrongAward, WrongAwardAdmin)