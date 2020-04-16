from django.contrib import admin
from .models import IncomingMessage, User, Quiz, Award, Message, Secret, WrongAward
from vk_utils import mailing_service
from .views import vk
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'first_name', 'state',
                    'created_at', 'last_quiz_solve', 'solving_mode')
    actions = ['reset_user', 'mailling']

    def reset_user(self, request, queryset):
        for obj in queryset:
            obj.state = "normal"
            obj.solving_mode = False
            obj.save()

    def mailling(self, request, queryset):
        with open("/shanfiles/text.txt", "r") as f:
            text = f.read()
        ids = []
        for obj in queryset:
            if obj.last_quiz_solve == 40:
                ids.append(obj.vk_id)

        for i in ids:
            try:
                mailing_service.MailingService.manual_send_message(
                    vk, i, text)
            except:
                print("Err", i)

        User.reset_users(ids)


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
