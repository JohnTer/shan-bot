from django import forms
from django.core.exceptions import ValidationError


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    message_type = models.CharField(max_length=255)
    from_id = models.IntegerField()

    text = models.CharField(max_length=4096)

    def __str__(self):
        return self.text
