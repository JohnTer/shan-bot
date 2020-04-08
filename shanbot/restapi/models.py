import time
import orjson
import dateparser
from django.db import models

USER_STATES = ('begin', 'start', 'hello',
               'greeting', 'normal', 'quiz', 'secret')


class IncomingMessage(models.Model):
    id = models.AutoField(primary_key=True)
    from_id = models.IntegerField()
    text = models.CharField(max_length=4096)

    def __str__(self):
        return self.text

    @classmethod
    def create(cls, json_object):
        from_id = json_object['object']['message']['from_id']
        text = json_object['object']['message']['text']

        driver = cls(from_id=from_id,
                     text=text)
        return driver


def get_time():
    return int(time.time())


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default='')
    vk_id = models.IntegerField(unique=True)
    state = models.CharField(max_length=255, default=USER_STATES[0])
    created_at = models.BigIntegerField(
        default=get_time, blank=True, help_text='format: Unix timestamp')
    last_quiz_solve = models.IntegerField(default=0)
    solving_mode = models.BooleanField(default=False)
    admin_mode = models.BooleanField(default=False)


    @classmethod
    def create(cls, vk_user_id, first_name="", last_name=""):
        return cls(first_name=first_name,
                   last_name=last_name,
                   vk_id=vk_user_id)

    @staticmethod
    def reset_users(user_list):
        def reset(u):
            blacklist = set(['begin', 'start', 'hello', 'greeting'])
            u.solving_mode = False
            u.state = USER_STATES[4] if u.state not in blacklist else u.state

        if not user_list:
            users = User.objects.all()
        else:
            users = User.objects.filter(vk_id__in=user_list)

        for user in users:
            reset(user)
            user.save()


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4100, blank=True, null=True)
    text = models.CharField(max_length=4100)
    answers_json = models.CharField(max_length=4100)
    award_id = models.ForeignKey(
        'Award', on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)
    attachments_json = models.CharField(max_length=4100, blank=True, null=True)

    available_unixtime = models.BigIntegerField(
        null=True, blank=True, default=0, help_text="format: Unix timestamp")
    available_strtime = models.CharField(
        max_length=255, default="26.04.2020 12:00")

    def save(self, *args, **kwargs):
        if not self.attachments_json:
            self.attachments_json = None
        if self.available_strtime:
            date = dateparser.parse(self.available_strtime, languages=['ru'])
            self.available_unixtime = date.timestamp()
        super(Quiz, self).save(*args, **kwargs)


class Award(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=4100)
    attachments_json = models.CharField(
        max_length=4100, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.attachments_json:
            self.attachments_json = None
        super(Award, self).save(*args, **kwargs)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message_type = models.CharField(max_length=255)
    text = models.CharField(max_length=4100)
    attachments_json = models.CharField(
        max_length=4100, null=True, blank=True, default=None)

    def __str__(self):
        return self.message_type

    def save(self, *args, **kwargs):
        if not self.attachments_json:
            self.attachments_json = None
        super(Message, self).save(*args, **kwargs)


class Secret(models.Model):
    id = models.AutoField(primary_key=True)
    secret_type = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    text = models.CharField(max_length=4100, null=True,
                            blank=True, default=None)
    attachments_json = models.CharField(
        max_length=4100, null=True, blank=True, default=None)

    available = models.BigIntegerField(
        null=True, blank=True, default=None, help_text="format: Unix timestamp")
    order_type = models.IntegerField(default=0)

    def __str__(self):
        return str(self.secret_type)

    def save(self, *args, **kwargs):
        if not self.attachments_json:
            self.attachments_json = None
        super(Secret, self).save(*args, **kwargs)


class MailingMessage(models.Model):
    id = models.AutoField(primary_key=True)
    command_type = models.CharField(max_length=255)
    text = models.CharField(max_length=4100)
    user_list = models.CharField(max_length=4100)
    attachments_json = models.CharField(
        max_length=4100, null=True, blank=True, default=None)

    available = models.BigIntegerField(
        null=True, blank=True, default=None, help_text="format: Unix timestamp")

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.attachments_json:
            self.attachments_json = None
        super(Secret, self).save(*args, **kwargs)
