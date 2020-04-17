from django.contrib import admin
from .models import IncomingMessage, User, Quiz, Award, Message, Secret, WrongAward
from vk_utils import mailing_service
from .views import vk
# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


class MyEmsAdminSite(AdminSite):
    site_title = ugettext_lazy("SHAN-BOT Beta version 0.6")
    site_header = ugettext_lazy("SHAN-BOT Beta version 0.6")
    index_title = ugettext_lazy("SHAN-BOT Beta version 0.6")

mas = MyEmsAdminSite()

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
            if obj.last_quiz_solve > 30:
                ids.append(obj.vk_id)

        for i in ids:
            try:
                mailing_service.MailingService.manual_send_message(
                    vk, i, text)
            except Exception as e:
                print("Err", i)

        User.reset_users(ids)


mas.register(User, UserAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('order', 'text',
                    'available_strtime', 'available_unixtime')


mas.register(Quiz, QuizAdmin)


class AwardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'attachments_json')


mas.register(Award, AwardAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_type', 'text', 'attachments_json')


mas.register(Message, MessageAdmin)


class SecretAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'available',
                    'order_type', 'attachments_json')


mas.register(Secret, SecretAdmin)


mas.register(IncomingMessage)


class WrongAwardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'attachments_json')


mas.register(WrongAward, WrongAwardAdmin)


