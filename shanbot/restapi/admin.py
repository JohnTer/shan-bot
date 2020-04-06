from django.contrib import admin
from .models import IncomingMessage, User, Quiz, Award, Message, Secret
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'first_name', 'state',
                    'created_at', 'last_quiz_solve', 'solving_mode')


admin.site.register(User, UserAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'order',
                    'available', )


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
