import time
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

import vk_api
import orjson
import requests
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from shanbot import settings
from vk_utils import text_message, quiz_message, mailing_service
from restapi import models
from .states import StateEngine, IncomingMessage
from .models import User


vk_session = vk_api.VkApi(
    token=settings.VK_API_TOKEN)
vk = vk_session.get_api()
confirmation_code = settings.VK_CONFIRMATION_CODE
secret_key = settings.VK_SECRET_KEY


A = StateEngine(vk)


@method_decorator(csrf_exempt, name='dispatch')
class EchoView(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        data = orjson.loads(request.body)
        if data["type"] == "confirmation":
            return HttpResponse(settings.VK_CONFIRMATION_CODE, status=200)
        current_time = int(time.time())
        send_time = data['object']['message']['date']
        if abs(current_time - send_time) > 20:  # ttl
            return HttpResponse('ok', status=200)

        message_class = IncomingMessage.create(data)
        A.execute(message_class)

        return HttpResponse('ok', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class MailingServiceView(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = orjson.loads(request.body)
        m_service = mailing_service.MailingService(vk, data)
        m_service.execute()
        User.reset_users(data['user_list'])
        return HttpResponse('ok', status=200)
